import {getTeiger} from "../requests.js"

const teigColors = [
    '#2f5f8f',
    '#496f94',
    '#5b7f9d',
    '#6f8fa8',
    '#3f6f86',
    '#55738a'
];

const teigHoverStyle = {
    weight: 4,
    opacity: 1,
    fillOpacity: 0.28
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

export function formatArea(areaM2) {
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

export function resetTeigInfoPanel(teigInfoPanel) {
    if (teigInfoPanel) {
        teigInfoPanel.update(0, 0);
    }
};

function numberTeigFeatures(features) {
    features.forEach((feature, index) => {
        feature.properties = feature.properties || {};
        feature.properties.teig_number = index + 1;
    });
};

function getTotalTeigArea(features) {
    return features.reduce((sum, feature) => {
        return sum + Number(feature.properties.area_m2 || 0);
    }, 0);
};

function updateTeigInfoPanel(teigInfoPanel, features) {
    if (teigInfoPanel) {
        teigInfoPanel.update(features.length, getTotalTeigArea(features));
    }
};

function bindTeigTooltip(feature, featureLayer) {
    const teigNumber = feature.properties.teig_number;
    const area = formatAreaM2(feature.properties.area_m2);

    featureLayer.bindTooltip(`Teig ${teigNumber} – ${area}`);
};

function bindTeigHover(feature, featureLayer) {
    featureLayer.on({
        mouseover: () => {
            featureLayer.setStyle(teigHoverStyle);
            featureLayer.bringToFront();
        },
        mouseout: () => {
            featureLayer.setStyle(getTeigStyle(feature));
        }
    });
};

function setupTeigFeature(feature, featureLayer) {
    bindTeigTooltip(feature, featureLayer);
    bindTeigHover(feature, featureLayer);
};

export function displayTeiger(lat, lng, r50Meter, layer, teigInfoPanel){
    getTeiger(lat, lng, r50Meter).then( data => {
        if (!Array.isArray(data.features)) {
            console.warn("Ingen teiger å tegne:", data);
            resetTeigInfoPanel(teigInfoPanel);
            return;
        }

        numberTeigFeatures(data.features);
        updateTeigInfoPanel(teigInfoPanel, data.features);

        L.geoJson(data, {
            style: getTeigStyle,
            onEachFeature: setupTeigFeature
        }).addTo(layer);
    }).catch(error => {
        console.error("Klarte ikke å hente teiger:", error);
        resetTeigInfoPanel(teigInfoPanel);
    })
};
