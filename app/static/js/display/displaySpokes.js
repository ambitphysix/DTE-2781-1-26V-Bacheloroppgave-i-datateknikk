import {getRadii, getSpokes, getSearchAreas} from "./requests.js"

export function displaySpokes(lat, lng, missingPersonCategory, layer){
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