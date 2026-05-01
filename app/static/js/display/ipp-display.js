export function displayIPP(lat, lng, layer){
    var icon = L.icon(
        {
            iconUrl: './static/css/images/ipp.png',
            iconSize: [15, 15]
        }
    )
    const marker = L.marker([lat, lng], {icon: icon})
    marker.bindTooltip("IPP")
    marker.addTo(layer);
};
