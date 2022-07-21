

const tokenID = 'pk.eyJ1IjoiamFkZXJzIiwiYSI6ImNsM2xhMDBtaTBtdnozb3JyMnlnemthMzMifQ.2_fFwIkLrKOq1ljbrBudYQ';
// map 
const mapStyle = "mapbox://styles/mapbox/streets-v11"
const qclongLat = [121.06171106766422,14.626033700189234]
const qcZoom = 14


mapboxgl.accessToken = tokenID

const _MBOX_MAP_CONFIG = {
    container: 'map', 
    style: mapStyle, 
    center: qclongLat, 
    zoom: qcZoom  
}

// DIRECTION
const _MBOX_DIRECTION_CONFIG = 
{
    accessToken: mapboxgl.accessToken,
    unit: 'metric',
    profile: 'mapbox/driving',
    alternatives: false,
    geometries: 'geojson',
    controls: { instructions: true },
    flyTo: false
}

// MAX ATTEMPT TO GENERATE ROUTES
const _MAXATTEMPS = 1


const theRoutePaint = {
    'line-color': 'red',
    'line-opacity': 1,
    'line-width': 13,
    'line-blur': 1
}


const theBoxPaint = {
    'fill-color': '#FFC300',
    'fill-opacity': 0.5,
    'fill-outline-color': '#FFC300'
}

