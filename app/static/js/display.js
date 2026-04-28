function displayMapObjects(eventHandler, ringLayer) {
    displayRings(
        eventHandler.latlng.lat,
        eventHandler.latlng.lng,
        ringLayer
    );
};

function displayRings(lat, lng, layer){
    layer.clearLayers();
    L.circle([lat, lng], {
        color: 'red',
        fillColor: 'rgb(255, 0, 0)',
        fillOpacity: 0.0,
        radius: 500
    }).addTo(layer);
}