export function getRadii(missingPersonCategory){
    return fetch(`/data/radii/${missingPersonCategory}`)
    .then(response =>
        {return response.json()}
    )
}

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

export function getSearchAreas(lat, lng, radius, minAreaValue, maxAreaValue){
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lng', lng);
    params.append('radius', radius);
    params.append('minAreaValue', minAreaValue);
    params.append('maxAreaValue', maxAreaValue);
    return fetch(`/data/searchAreas?${params}`)
    .then(response =>
        {return response.json()}
    )
}