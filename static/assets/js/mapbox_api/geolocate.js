
const mapBoxGeolocate = () => {
    // Initialize the GeolocateControl.
    const geolocate = new mapboxgl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
            },
        trackUserLocation: true,
        showUserHeading: true
    });

    return geolocate;
}