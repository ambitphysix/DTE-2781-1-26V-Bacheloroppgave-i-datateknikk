/* 
En egendefinert Leaflet-kontroll (UI-komponent) som legger til et input-skjema for minimums- og maksimumsareal i kartet.
*/

export const MinMaxAreaMenu = L.Control.extend({
    options: {
        position: 'topright'
    },

    onAdd: function() {
        var form = L.DomUtil.create('form', 'minmaxAreaMenu');
        form.id = "minmaxAreaMenu"
        form.innerHTML = `
            <input type="number" id="minArea" placeholder="Min Area" class="area-input">
            <input type="number" id="maxArea" placeholder="Max Area" class="area-input">
        `
        L.DomEvent.disableClickPropagation(form);
        L.DomEvent.disableScrollPropagation(form);
        return form
    },

    onRemove: function(map) {
        // Nothing to do here
    }
});