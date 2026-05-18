import {getRadii, getSpokes, getSearchAreas} from "./requests.js"

/**Henter og tegner opp ledelinjer (spokes) på kartet basert på IPP og kategorien til den savnede.**/

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