import {getSpokes} from "../requests.js"

export function displaySpokes(lat, lng, layer){
    getSpokes(lat, lng).then( data => {
        data.forEach( spoke => {
                L.geoJson(spoke).addTo(layer);
        }
        )
    })
};
