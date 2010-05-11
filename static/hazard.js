
function loadMap(div) { 
  Ext.onReady(function(){ 
    map = new OpenLayers.Map(div);
    layer = new OpenLayers.Layer.OSM("Simple OSM Map");
    map.addLayer(layer);
    map.setCenter(new OpenLayers.LonLat(-8051914,2104311),10)
  })

}

var pdfs, map; 
function printMaps() { 
    Ext.onReady(function(){ 
      var options = {
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                maxResolution: 156543.0339,
                maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,
                                                 20037508.34, 20037508.34)
                  };
      map = new OpenLayers.Map(options);
      var layer = new OpenLayers.Layer.OSM("Simple OSM Map");
      pdfs = new OpenLayers.Layer.Vector("PDF Layer");
      
      map.addLayers([layer,pdfs]);

      new GeoExt.MapPanel({
        renderTo: 'map',
        height: 250,
        width: window.outerWith,
        layout: 'fit',
        map: map
      });

      map.setCenter(new OpenLayers.LonLat(-8051914,2104311),10)
      store = new GeoExt.data.FeatureStore({
        layer: pdfs,
        fields: [
            {name: 'name', type: 'string'},
        ],
        proxy: new GeoExt.data.ProtocolProxy({
          protocol: new OpenLayers.Protocol.HTTP({
                url: "/hazard/maps.json",
                format: new OpenLayers.Format.GeoJSON()
            })
        }),
        autoLoad: true
    });
     gridPanel = new Ext.grid.GridPanel({
       renderTo: "pdf-grid",
        store: store,
       height: 400,
        columns: [{
            header: "Name",
            dataIndex: "name"
        }],
        sm: new GeoExt.grid.FeatureSelectionModel() 
    });

    });}
