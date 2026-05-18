import {getRadii, getSpokes, getSearchAreas} from "./requests.js"

/**Henter og tegner opp søketeiger på kartet basert på IPP, kategorien til den savnede og ønsket teigstørrelse.**/

export function displaySearchAreas(lat, lng, missingPersonCategory, layer, minAreaValue, maxAreaValue){
    layer.clearLayers();
    getRadii(missingPersonCategory).then( radius => {
        getSearchAreas(lat, lng, radius.p75*1000, minAreaValue, maxAreaValue).then( data => {
            layer.addData(data)
            }
            )
        }
    )
};