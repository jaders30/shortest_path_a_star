const popup = (map) => {

    // When a click event occurs on a feature in the places layer, open a popup at the
    // location of the feature, with description HTML from its properties.
    map.on('click', 'places', (e) => {
        // Copy coordinates array.
        const coordinates = e.features[0].geometry.coordinates.slice();
        const description = e.features[0].properties.description;
        
        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }
 
        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    });

    // Change the cursor to a pointer when the mouse is over the places layer.
    map.on('mouseenter', 'places', () => {
        map.getCanvas().style.cursor = 'pointer';
    });
     
    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'places', () => {
        map.getCanvas().style.cursor = '';
    });
    
    return map;
}
// const popup = (map) => {
//     const popup = new mapboxgl.Popup({
//         closeButton: false,
//         closeOnClick: false
//     });

//     map.on('mouseenter', 'places', (e) => {
//         // Change the cursor style as a UI indicator.
//         map.getCanvas().style.cursor = 'pointer';

//         // Copy coordinates array.
//         const coordinates = e.features[0].geometry.coordinates.slice();
//         const description = e.features[0].properties.description;

//         // Ensure that if the map is zoomed out such that multiple
//         // copies of the feature are visible, the popup appears
//         // over the copy being pointed to.
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }

//         // Populate the popup and set its coordinates
//         // based on the feature found.
//         popup.setLngLat(coordinates).setHTML(description).addTo(map);
//     });

//     map.on('mouseleave', 'places', () => {
//         map.getCanvas().style.cursor = '';
//         popup.remove();
//     });
//     return map;
// }