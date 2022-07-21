(async function () {

    "use strict";

    // MAP OBJECT
    let map = new mapboxgl.Map(_MBOX_MAP_CONFIG);

    // DIRECTION OBJECT
    const directions = new MapboxDirections(_MBOX_DIRECTION_CONFIG);
    const geolocate = mapBoxGeolocate();

    map.addControl(geolocate, 'bottom-right');
    map.addControl(directions, 'top-right');
    map.scrollZoom.enable();


    let bbox = [0, 0, 0, 0];
    let polygon = turf.bboxPolygon(bbox);


    // initialize the map
    map.on('load', () => {
        hide(document.querySelectorAll('.directions-control-instructions'));
        $('#preloader').remove();
    });


    let isOpenRecomendationBtn = true;
    document.getElementById('showRecommedationBtn').addEventListener("click", (event) => {

        if (isOpenRecomendationBtn) {
            hide(document.querySelectorAll('.card_recommendations'));
            document.getElementById("showRecommedationBtn").style.background = '#09677c';
            document.getElementById("showRecommedationBtn").style.color = 'white';
            isOpenRecomendationBtn = false
        } else {
            show(document.querySelectorAll('.card_recommendations'));
            document.getElementById("showRecommedationBtn").style.background = 'white';
            document.getElementById("showRecommedationBtn").style.color = '#09677c';
            isOpenRecomendationBtn = true
        }

    });

    document.getElementById('clearRoutesBtn').addEventListener("click", (event) => {
        removeAllSearchRoute();
    });

    const removeAllSearchRoute = () => {
        hide(document.querySelectorAll('.card_recommendations'));
        directions.removeRoutes();
        isSolutionFound = false;
        reports.innerHTML = ''

        // Remove origin after clicking clear search
        var parentOrigin = document.getElementById('mapbox-directions-origin-input');
        var firstchildrenOrigin = parentOrigin.children[0];
        var childrenOrigin = firstchildrenOrigin.children[1];
        childrenOrigin.value = "";

        // Remove close icon on origin
        var childrenPinRightOrigin = firstchildrenOrigin.children[3];
        var theCloseIconOrigin = childrenPinRightOrigin.children[0];
        theCloseIconOrigin.classList.remove("active");

        // Remove destination after clicking clear search
        var parentDestination = document.getElementById('mapbox-directions-destination-input');
        var firstchildrenDestination = parentDestination.children[0];
        var childrenDestination = firstchildrenDestination.children[1];
        childrenDestination.value = "";

        // Remove close icon on destination
        var childrenPinRightDestination = firstchildrenDestination.children[3];
        var theCloseIconDestination = childrenPinRightDestination.children[0];
        theCloseIconDestination.classList.remove("active");
    }

   

    
    const generateResultPath = (resultPath) => {
        resultPath.forEach((coord, index) => {
            if (index === 0) {
                directions.setOrigin(coord);
            }
            else if (index === resultPath.length - 1) {
                directions.setDestination(coord);
            } else {
                directions.addWaypoint(index - 1, coord);
            }
        });
    }




    let counter = 0;
    const maxAttempts = _MAXATTEMPS;
    const reports = document.getElementById('reports');
    let lisOfAllRoutes = [];
    let isSolutionFound = false;
    let eventRouteTemp = {}

    const generateReports = (res) => {

        if (res != null) {           
            addCard('shortest_route',
                reports,
                "Shortest Route",
                res["shortest_route"].weight);

            document.getElementById(`shortest-route-btn`).addEventListener("click", (e) => {
                directions.removeRoutes();
                generateResultPath(res["shortest_route"].path);
            });

            show(document.querySelectorAll('.card_recommendations'));
        }
    }

    const finalOperation = async () => {
        counter = 0;

        const dataToServer = {
            // "displayedObstacles": displayedObstacles,
            "lisOfAllRoutes": lisOfAllRoutes
        };

        try {
            // SEND ALL POSSIBLE ROUTES
            console.log(dataToServer);
            const res = await sendAllPossibleRoutes(dataToServer);
            lisOfAllRoutes = [];
            directions.removeRoutes();
            isSolutionFound = true;
                
            console.log("Data: Successfully sent to server!");
            return res;
        } catch (err) {
            console.log("Error: Something went wrong sending data to server!");
            return null;
        }
    }


    const diplsayRouteInstruction = (data) => {

        const instructions = document.getElementById('instructions');
        instructions.innerHTML = ``;

        const legs = data[0].legs;
        let tripInstructions = '';

        for (const leg of legs) {

            const steps = leg.steps;
            for (const step of steps) {
                tripInstructions += `<li><p>${step.maneuver.instruction}</p></li>`;
                tripInstructions += `<br>`;
            }
        }
        instructions.innerHTML += `<div class="instruction_header">${Math.floor(
            data[0].duration / 60
        )} min 🚘</div>`;


        instructions.innerHTML += `<ol>${tripInstructions}</ol>`;


    }

    directions.on('route', async (event) => {
        console.log(event.route)
        eventRouteTemp = event.route;

        // uncomment displayRouteInstruction(eventRouteTemp) if you want to display the
        // directions feature of the application
        // diplsayRouteInstruction(eventRouteTemp);
        // print the entire route details on console
        // console.log(event.route)
        if (!isSolutionFound) {
            // uncomment this if you want to display directions feature
            // isOpenDirectionBtn = true;
            const summaryRoutes = await routeResults(event.route);
            lisOfAllRoutes.push(...summaryRoutes);
            document.getElementById("preloaderRoute").style.display = "flex";
            $('#preloaderRoute').show();
            for (const route of summaryRoutes) {

                // Get GeoJSON LineString feature of route
                const routeLine = polyline.toGeoJSON(route.geometry);
                // Create a bounding box around this route
                // The app will find a random point in the new bbox
                bbox = turf.bbox(routeLine);
                polygon = turf.bboxPolygon(bbox);
                // check the current routeline touches obstacle.
                // let brgyObsHits = [];

                // allObstacle.forEach((obs, routes_idx) => {
                //     if (!turf.booleanDisjoint(obs[4], routeLine)) {
                //         brgyObsHits.push(obs[0]);
                //     }
                // });

                if (counter >= maxAttempts) {
                    const res = await finalOperation();
                    // generate recommendation...
                    generateReports(res);
                    $('#preloaderRoute').hide();
                    return;
                }
                else {
                    counter = counter + 1;
                    // As the attempts increase, expand the search area
                    // by a factor of the attempt count
                    polygon = turf.transformScale(polygon, counter * 0.01);
                    bbox = turf.bbox(polygon);
                    // Add a randomly selected waypoint to get a new route from the Directions API
                    const randomWaypoint = turf.randomPoint(1, { bbox: bbox });
                    console.log(randomWaypoint);

                    directions.setWaypoint(0, randomWaypoint['features'][0].geometry.coordinates);
                }
            }
            console.log(`we are at ${counter} of generating routes`);
        }
    });


    window.addEventListener("error", async (e) => {
        // send all data if there are errors happened.
        // so we can save more request.
        if (counter > 0 && counter <= maxAttempts) {
            finalOperation();
        }
    });


})()