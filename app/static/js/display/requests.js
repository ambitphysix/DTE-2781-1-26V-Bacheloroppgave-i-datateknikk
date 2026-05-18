/* 
Funksjoner som benyttes av display-funksjonene for å hente data fra databasene.
*/

//Henter radiuser for sirkler i sykkelhjulmodellen basert på savnetkategori.
export function getRadii(missingPersonCategory){ 
    return fetch(`/data/radii/${missingPersonCategory}`)
    .then(response =>
        {return response.json()}
    )
}

//Henter eiker i sykkelhjulmodellen basert på IPP og avgrensende radius.
export function getSpokes(lat, lng, radius){
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lng', lng);
    params.append('radius', radius);
    return fetch(`/data/spokes?${params}`)
    .then(response =>
        {return response.json()}
    )
}

//Henter søketeiger/polygoner basert på IPP, radius og ønsket minimums- og maksimumsstørrelse.
export function getSearchAreas(lat, lng, radius, minAreaValue, maxAreaValue){
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lng', lng);
    params.append('radius', radius);
    params.append('minAreaValue', minAreaValue);
    params.append('maxAreaValue', maxAreaValue);
    return fetch(`/data/polygons?${params}`)
    .then(response =>
        {return response.json()}
    )
}