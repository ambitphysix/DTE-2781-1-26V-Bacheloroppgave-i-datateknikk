export function displayRings(lat, lng, layer, missingPersonCategory){
    layer.clearLayers();
    getRadii(missingPersonCategory).then( data => {
            L.circle([lat, lng], {
            color: 'red',
            fillColor: 'rgb(255, 0, 0)',
            fillOpacity: 0.0,
            radius: data.p25*1000
            }).addTo(layer);

            L.circle([lat, lng], {
            color: 'red',
            fillColor: 'rgb(255, 0, 0)',
            fillOpacity: 0.0,
            radius: data.p50*1000
            }).addTo(layer);

            L.circle([lat, lng], {
            color: 'red',
            fillColor: 'rgb(255, 0, 0)',
            fillOpacity: 0.0,
            radius: data.p75*1000
            }).addTo(layer);

    
            L.circle([lat, lng], {
            color: 'red',
            fillColor: 'rgb(255, 0, 0)',
            fillOpacity: 0.0,
            radius: data.p95*1000
            }).addTo(layer)
        }
    )    
};

export function displayIPP(lat, lng, layer){
    var icon = L.icon(
        {
            iconUrl: './static/css/images/ipp.png',
            iconSize: [15, 15]
        }
    )
    const marker = L.marker([lat, lng], {icon: icon})
    marker.bindTooltip("IPP");
    marker.addTo(layer);
};