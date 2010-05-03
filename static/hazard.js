
function loadMap() { 
  map = new OpenLayers.Map('hazard-map');
  layer = new OpenLayers.Layer.OSM("Simple OSM Map");
  map.addLayer(layer);
  map.setCenter(new OpenLayers.LonLat(-8051914,2104311),10)

}
