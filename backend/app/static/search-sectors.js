function createSearchSectorLayer(map) {
  var layer = L.layerGroup().addTo(map);

  function draw(lat, lng) {
    layer.clearLayers();

    var sectorAngle = 360 / SAR_MAP_CONFIG.searchSectors.count;

    for (var index = 0; index < SAR_MAP_CONFIG.searchSectors.count; index++) {
      var startBearing = index * sectorAngle;
      var endBearing = startBearing + sectorAngle;
      var points = createSectorPoints(lat, lng, startBearing, endBearing);

      L.polygon(points, {
        color: SAR_MAP_CONFIG.searchSectors.color,
        fillColor: SAR_MAP_CONFIG.searchSectors.fillColor,
        fillOpacity: SAR_MAP_CONFIG.searchSectors.fillOpacity,
        weight: 1,
        interactive: true,
      })
        .bindTooltip("Sektor " + (index + 1), {
          sticky: true,
          direction: "top",
        })
        .addTo(layer);
    }
  }

  function createSectorPoints(lat, lng, startBearing, endBearing) {
    var points = [[lat, lng]];
    var bearingStep =
      (endBearing - startBearing) / SAR_MAP_CONFIG.searchSectors.arcSteps;

    for (var step = 0; step <= SAR_MAP_CONFIG.searchSectors.arcSteps; step++) {
      var bearing = startBearing + bearingStep * step;
      points.push(
        destinationPoint(
          lat,
          lng,
          bearing,
          SAR_MAP_CONFIG.searchSectors.radius
        )
      );
    }

    return points;
  }

  return {
    draw: draw,
    clear: function () {
      layer.clearLayers();
    },
  };
}

function destinationPoint(lat, lng, bearing, distanceMeters) {
  var earthRadiusMeters = 6371000;
  var angularDistance = distanceMeters / earthRadiusMeters;
  var bearingRadians = toRadians(bearing);
  var latRadians = toRadians(lat);
  var lngRadians = toRadians(lng);

  var destinationLatRadians = Math.asin(
    Math.sin(latRadians) * Math.cos(angularDistance) +
      Math.cos(latRadians) *
        Math.sin(angularDistance) *
        Math.cos(bearingRadians)
  );

  var destinationLngRadians =
    lngRadians +
    Math.atan2(
      Math.sin(bearingRadians) *
        Math.sin(angularDistance) *
        Math.cos(latRadians),
      Math.cos(angularDistance) -
        Math.sin(latRadians) * Math.sin(destinationLatRadians)
    );

  return [toDegrees(destinationLatRadians), toDegrees(destinationLngRadians)];
}

function toRadians(degrees) {
  return (degrees * Math.PI) / 180;
}

function toDegrees(radians) {
  return (radians * 180) / Math.PI;
}
