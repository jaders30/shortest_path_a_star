function hide (elements) {
    elements = elements.length ? elements : [elements];
    for (var index = 0; index < elements.length; index++) {
        elements[index].style.display = 'none';
    }
}
function show (elements) {
    elements = elements.length ? elements : [elements];
    for (var index = 0; index < elements.length; index++) {
        elements[index].style.display = 'block';
    }
}

const labeltheWeight = (id) => {
    if(id === "shortest_route")
        return "distance";
}

function addCard(id, element, detail, bottom_detail) {
       
    const card = document.createElement('div');
    card.className = `card`;
    card.setAttribute("id", `id-${id}-card`);
       

       
    const heading = document.createElement('div');
    heading.setAttribute("id", `${id}-header`);
        
    heading.className = 'card-header route-found';
    heading.innerHTML = `Route Found ✔️ <span class="badge bg-info">Recommended</span>`;
        
    
    
    const details = document.createElement('div');
    details.className = 'card-details';
    details.innerHTML = `${detail}. 🚘  <span><button id="shortest-route-btn" type="button" class="btn  py-0 btn-sm btn-outline-primary active">select</button></span>`;
       
    

    const bottomCardDetails = document.createElement('div');
    bottomCardDetails.className = 'weight-details';
    bottomCardDetails.innerHTML = `Weight: ${bottom_detail.toFixed(2)} | considering the ${labeltheWeight(id)}.`;

       
        
        
    card.appendChild(heading);
    card.appendChild(details);
    card.appendChild(bottomCardDetails);
      

    element.insertBefore(card, element.firstChild);
}




// this is for printing the marker for coordinates
// only for the documentation of the step-by-step
// computation of the route
const generateGEOJSONMarkers = (coordinates) => {
    let finalgeojson = {
        'type': 'FeatureCollection',
        'features': []
    };
   


    for(var i = 0; i < coordinates.length; i++) {
        var lang = coordinates[i][0];
        var lat  = coordinates[i][1];
        let objectOfPoints = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': []
            },
            'properties': {
                'title': 'Latitude & Longittude',
                'description': []
            }
        }
        objectOfPoints['geometry']['coordinates'] = [lang, lat]
        objectOfPoints['properties']['description'] = [lang, lat]
        finalgeojson['features'].push(objectOfPoints)
    }

    return finalgeojson;
}

var bboxst = [0, 0, 1000, 1000];
    const createObstacles = (newclearances) => {
        console.log("Clearances",newclearances)
        newallObstacle = []
        for(let i = 0; i < newclearances["features"].length; i++){
            const obs = turf.polygon(newclearances["features"][i]['geometry']['coordinates']);
            const nameBrgy = newclearances["features"][i]['properties']['brgy_name'];
            const activeCs = newclearances["features"][i]['properties']['active_cases'];
            const totalCs = newclearances["features"][i]['properties']['total_cases'];
            const population = newclearances["features"][i]['properties']['population'];
            
            // [barangay name, obstacle object]
            newallObstacle.push([nameBrgy, activeCs, totalCs,  population, turf.bboxClip(obs, bboxst)])      
        }
        return newallObstacle;
    }

const routeResults = (listofRoutes) => {
    let routes_result = []
    // scan all routes
    for(let route = 0; route < listofRoutes.length; route++){
        
        // create dictionary
        routes_result[route] = {}
        const currentRoute = listofRoutes[route]; // current route

        routes_result[route]["geometry"] = currentRoute.geometry
        const legs = currentRoute.legs;  // get legs
        
        routes_result[route]["step_locations"] = []
        // loop through each legs
        for(let leg = 0; leg < legs.length; leg++){
            
            const currentLeg =  legs[leg]; // current leg
            const currentSteps = currentLeg.steps; // get leg steps
           
            for(let step = 0; step < currentSteps.length; step++){

                const location_coord = currentSteps[step].maneuver.location;
                // nodes - coordinates and weights
                routes_result[route]["step_locations"].push({
                    "location" : location_coord,
                    "covid_weight" : 0,
                    "active_covid_weight": 0
                })
               
            }      
        }    
    }

    
    // routes_result.forEach((current_summary_route, routes_idx) => {

    //     const nodes_path = current_summary_route["step_locations"];

    //     nodes_path.forEach((current_node, node_idx) => {

    //         // coordinates
    //         const currentCoord = current_node["location"] 

    //         // convert coordinates to turf point objects
    //         const currentLocTurf = turf.point(currentCoord); 

    //         // Check each node if hits obstacle to put
    //         // covid weights. 
    //         allObstacle.forEach((obs, idxObs) => {

    //             if(!turf.booleanDisjoint(obs[4], currentLocTurf)){

    //                 // put the corresponding weights each node
    //                 routes_result[routes_idx]["step_locations"][node_idx]["covid_weight"] = obs[2]
    //                 routes_result[routes_idx]["step_locations"][node_idx]["active_covid_weight"] = obs[1]
    //                 routes_result[routes_idx]["step_locations"][node_idx]["barangay_name"] = obs[0]
    //             }
    //         });
    //     });
    // });
 
    return routes_result;
}
  