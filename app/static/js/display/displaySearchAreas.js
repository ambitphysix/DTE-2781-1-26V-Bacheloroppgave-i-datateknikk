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