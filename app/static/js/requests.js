export function getRadii(missingPersonCategory){
    return fetch(`/data/radii/${missingPersonCategory}`)
    .then(response =>
        {return response.json()}
    )
}

export function getSpokes(lat, lng){
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lng', lng);
    return fetch(`/data/spokes?${params}`)
    .then(response =>
        {return response.json()}
    )
}

export function getTeiger(lat, lng, r50Meter, extendMeter = 50){
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lng', lng);
    params.append('r50_meter', r50Meter);
    params.append('extend_meter', extendMeter);
    return fetch(`/data/teiger?${params}`)
    .then(response =>
        {return response.json()}
    )
}
