import {getRadii, getSpokes, getSearchAreas} from "./requests.js"
import {displayRings, displayIPP} from "./displayRings.js"
import {displaySpokes} from "./displaySpokes.js"
import {displaySearchAreas} from "./displaySearchAreas.js"


export function displayMapObjects(eventHandler, ringLayer, spokeLayer, searchAreaLayer, minAreaValue, maxAreaValue, missingPersonCategory) {
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
        searchAreaLayer,
        minAreaValue,
        maxAreaValue
    );
};

