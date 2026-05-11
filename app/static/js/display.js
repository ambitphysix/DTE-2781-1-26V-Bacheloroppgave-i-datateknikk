import {getRadii} from "./requests.js"
import {getSpokes} from "./requests.js"
import {getSearchAreas} from "./requests.js"

export function displayMapObjects(eventHandler, ringLayer, spokeLayer, searchAreaLayer, missingPersonCategory) {
    displayRings(
        eventHandler.latlng.lat,
        eventHandler.latlng.lng,
        ringLayer,
        missingPersonCategory
    );

    displayIPP(
        eventHandler.latlng.lat,
        eventHandler.latlng.lng,
        ringLayer
    );

    displaySpokes(
        eventHandler.latlng.lat,
        eventHandler.latlng.lng,
        missingPersonCategory,
        spokeLayer
    );

    displaySearchAreas(
        eventHandler.latlng.lat,
        eventHandler.latlng.lng,
        missingPersonCategory,
        searchAreaLayer
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
};

function displayIPP(lat, lng, layer){
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

function displaySpokes(lat, lng, missingPersonCategory, layer){
    layer.clearLayers();
    getRadii(missingPersonCategory).then( radius => {
        getSpokes(lat, lng, radius.p75*1000).then( data => {
            data.forEach( spoke => {
                    layer.addData(spoke.geometry);
            }
            )
        })
        }
    )
};

function displaySearchAreas(lat, lng, missingPersonCategory, layer){
    layer.clearLayers();
    getRadii(missingPersonCategory).then( radius => {
        getSearchAreas(lat, lng, radius.p75*1000).then( data => {
            layer.addData(data)
            }
            )
        }
    )
};

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
