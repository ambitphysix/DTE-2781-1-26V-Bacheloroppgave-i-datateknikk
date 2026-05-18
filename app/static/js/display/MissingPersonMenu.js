/* 
En egendefinert Leaflet-kontroll (UI-komponent) som legger til et seleksjon av savnetkategori i kartet.
*/

export const MissingPersonMenu = L.Control.extend({
    onAdd: function(missingPersonCategories) {
        var select = L.DomUtil.create('select', 'missingPersonCategoryMenu');
        select.id = "missingPersonCategoryMenu"
        fetch('/data/missingPersonCategories')
            .then(response => response.json())
            .then(data => {
                select.innerHTML = '';
                data.forEach(category => {
                    select.innerHTML = select.innerHTML + `<option value="${category.kategori}">${category.kategori}</option>`;
                })
            }
        )
        L.DomEvent.disableClickPropagation(select);
        L.DomEvent.disableScrollPropagation(select);
        return select
    },

    onRemove: function(map) {
        // Nothing to do here
    }
});