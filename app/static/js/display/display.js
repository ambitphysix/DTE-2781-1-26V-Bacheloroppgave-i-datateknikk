import {displayRings} from "./rings-display.js"
import {displayIPP} from "./ipp-display.js"
import {displaySpokes} from "./spokes-display.js"
import {displayTeiger, resetTeigInfoPanel} from "./teiger-display.js"

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
        resetTeigInfoPanel(teigInfoPanel);
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
