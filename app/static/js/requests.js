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