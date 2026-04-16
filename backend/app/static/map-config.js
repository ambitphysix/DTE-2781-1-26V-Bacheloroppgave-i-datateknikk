var SAR_MAP_CONFIG = {
  startPosition: [59.91, 10.75],
  startZoom: 12,
  kartverketWmsUrl: "https://wms.geonorge.no/skwms1/wms.topo",
  kartverketLayer: {
    layers: "topo",
    format: "image/png",
    opacity: 0.8,
    attribution: "&copy; Kartverket",
  },
  searchZones: [
    { radius: 3000, color: "yellow", label: "75% Sone (Ytre)" },
    { radius: 1500, color: "orange", label: "50% Sone (Midtre)" },
    { radius: 500, color: "red", label: "25% Sone (Indre)" },
  ],
};
