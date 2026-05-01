import {formatArea} from "./teiger-display.js"

export const TeigInfoPanel = L.Control.extend({
    options: {
        position: 'topright'
    },

    onAdd: function(map) {
        this.container = L.DomUtil.create('div', 'teig-info-panel');
        L.DomEvent.disableClickPropagation(this.container);
        L.DomEvent.disableScrollPropagation(this.container);
        this.update(0, 0);
        return this.container;
    },

    update: function(teigCount, totalAreaM2) {
        if (!this.container) {
            return;
        }

        this.container.innerHTML = `
            <div class="teig-info-title">Søketeiger</div>
            <div class="teig-info-row">
                <span>Antall</span>
                <strong>${teigCount}</strong>
            </div>
            <div class="teig-info-row">
                <span>Areal</span>
                <strong>${formatArea(totalAreaM2)}</strong>
            </div>
        `;
    }
});
