function createSearchZoneLayer(map) {
  var layer = L.layerGroup().addTo(map);

  function draw(lat, lng) {
    layer.clearLayers();

    SAR_MAP_CONFIG.searchZones.forEach(function (zone) {
      L.circle([lat, lng], {
        radius: zone.radius,
        color: zone.color,
        fillColor: zone.color,
        fillOpacity: 0.05,
        weight: 2,
        dashArray: "5, 5",
        interactive: true,
      })
        .bindTooltip(zone.label, {
          sticky: true,
          direction: "top",
        })
        .addTo(layer);
    });
  }

  return {
    draw: draw,
    clear: function () {
      layer.clearLayers();
    },
  };
}
