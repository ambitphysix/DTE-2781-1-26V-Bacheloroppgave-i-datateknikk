import {getRadii} from "./requests.js"

export function displayMapObjects(eventHandler, ringLayer, missingPersonCategory) {
    displayRings(
        eventHandler.latlng.lat,
        eventHandler.latlng.lng,
        ringLayer,
        missingPersonCategory
    );
};

function displayRings(lat, lng, layer, missingPersonCategory){
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
}

export const MissingPersonMenu = L.Control.extend({
    onAdd: function(missingPersonCategories) {
        var select = L.DomUtil.create('select', 'missingPersonCategoryMenu');
        select.id = "missingPersonCategoryMenu"
        fetch('/data/missingPersonCategories')
            .then(response => response.json())
            .then(data => {
                select.innerHTML = '';
                data.forEach(category => {
                    select.innerHTML = select.innerHTML + `<option value="${category.kategori}">${category.kategori}</option>`;
                })
            }
        )
        L.DomEvent.disableClickPropagation(select);
        L.DomEvent.disableScrollPropagation(select);
        return select
    },

    onRemove: function(map) {
        // Nothing to do here
    }
});