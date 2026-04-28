export function getRadii(missingPersonCategory){
    return fetch(`/data/radii/${missingPersonCategory}`)
    .then(response =>
        {return response.json()}
    )
}