var map = L.map("map").setView(
  SAR_MAP_CONFIG.startPosition,
  SAR_MAP_CONFIG.startZoom
);

L.tileLayer.wms(
  SAR_MAP_CONFIG.kartverketWmsUrl,
  SAR_MAP_CONFIG.kartverketLayer
).addTo(map);

var ippMarker;
var searchZoneLayer = createSearchZoneLayer(map);

function setIpp(lat, lng) {
  if (ippMarker) {
    map.removeLayer(ippMarker);
  }

  ippMarker = L.marker([lat, lng]).addTo(map);
  ippMarker.bindPopup("<b>IPP satt</b><br>Søkesoner generert.").openPopup();

  searchZoneLayer.draw(lat, lng);
}

map.on("click", function (event) {
  setIpp(event.latlng.lat, event.latlng.lng);
});
