import {getRadii} from "../requests.js"

export function displayRings(lat, lng, layer, missingPersonCategory){
    layer.clearLayers();
    return getRadii(missingPersonCategory).then( data => {
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

            return data;
        }
    )    
};
