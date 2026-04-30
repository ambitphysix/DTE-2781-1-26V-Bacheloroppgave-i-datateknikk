import {getRadii} from "./requests.js"
import {getSpokes} from "./requests.js"
import {getTeiger} from "./requests.js"

const teigColors = [
    '#2f5f8f',
    '#496f94',
    '#5b7f9d',
    '#6f8fa8',
    '#3f6f86',
    '#55738a'
];

export function displayMapObjects(eventHandler, ringLayer, missingPersonCategory, teigInfoPanel) {
    const lat = eventHandler.latlng.lat;
    const lng = eventHandler.latlng.lng;

    displayRings(
        lat,
        lng,
        ringLayer,
        missingPersonCategory
    ).then(data => {
        displayTeiger(
            lat,
            lng,
            data.p50 * 1000,
            ringLayer,
            teigInfoPanel
        );
    }).catch(error => {
        console.error("Klarte ikke å hente søkeringer:", error);
        if (teigInfoPanel) {
            teigInfoPanel.update(0, 0);
        }
    });

    displayIPP(
        lat,
        lng,
        ringLayer
    );

    displaySpokes(
        lat,
        lng,
        ringLayer
    );
};

function displayRings(lat, lng, layer, missingPersonCategory){
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

function displayIPP(lat, lng, layer){
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

function displaySpokes(lat, lng, layer){
    getSpokes(lat, lng).then( data => {
        data.forEach( spoke => {
                L.geoJson(spoke).addTo(layer);
        }
        )
    })
};

function getTeigStyle(feature) {
    const teigNumber = feature.properties.teig_number || 1;
    const color = teigColors[(teigNumber - 1) % teigColors.length];

    return {
        color: color,
        weight: 2,
        opacity: 0.88,
        fillColor: color,
        fillOpacity: 0.12 + ((teigNumber % 3) * 0.03)
    };
};

function formatArea(areaM2) {
    const area = Number(areaM2 || 0);

    if (area >= 1000000) {
        return `${(area / 1000000).toLocaleString('nb-NO', {
            maximumFractionDigits: 2
        })} km²`;
    }

    return `${Math.round(area).toLocaleString('nb-NO')} m²`;
};

function formatAreaM2(areaM2) {
    return `${Math.round(Number(areaM2 || 0)).toLocaleString('nb-NO')} m²`;
};

export const TeigInfoPanel = L.Control.extend({
    options: {
        position: 'topright'
    },

    onAdd: function(map) {
        this.container = L.DomUtil.create('div', 'teig-info-panel');
        L.DomEvent.disableClickPropagation(this.container);
        L.DomEvent.disableScrollPropagation(this.container);
        this.update(0, 0);
        return this.container;
    },

    update: function(teigCount, totalAreaM2) {
        if (!this.container) {
            return;
        }

        this.container.innerHTML = `
            <div class="teig-info-title">Søketeiger</div>
            <div class="teig-info-row">
                <span>Antall</span>
                <strong>${teigCount}</strong>
            </div>
            <div class="teig-info-row">
                <span>Areal</span>
                <strong>${formatArea(totalAreaM2)}</strong>
            </div>
        `;
    }
});

function displayTeiger(lat, lng, r50Meter, layer, teigInfoPanel){
    getTeiger(lat, lng, r50Meter).then( data => {
        if (!data.features) {
            console.warn("Ingen teiger å tegne:", data);
            if (teigInfoPanel) {
                teigInfoPanel.update(0, 0);
            }
            return;
        }

        data.features.forEach((feature, index) => {
            feature.properties = feature.properties || {};
            feature.properties.teig_number = index + 1;
        });

        const totalArea = data.features.reduce((sum, feature) => {
            return sum + Number(feature.properties.area_m2 || 0);
        }, 0);

        if (teigInfoPanel) {
            teigInfoPanel.update(data.features.length, totalArea);
        }

        L.geoJson(data, {
            style: getTeigStyle,
            onEachFeature: (feature, featureLayer) => {
                const teigNumber = feature.properties.teig_number;
                const area = formatAreaM2(feature.properties.area_m2);

                featureLayer.bindTooltip(`Teig ${teigNumber} – ${area}`);

                featureLayer.on({
                    mouseover: () => {
                        featureLayer.setStyle({
                            weight: 4,
                            opacity: 1,
                            fillOpacity: 0.28
                        });
                        featureLayer.bringToFront();
                    },
                    mouseout: () => {
                        featureLayer.setStyle(getTeigStyle(feature));
                    }
                });
            }
        }).addTo(layer);
    }).catch(error => {
        console.error("Klarte ikke å hente teiger:", error);
        if (teigInfoPanel) {
            teigInfoPanel.update(0, 0);
        }
    })
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
