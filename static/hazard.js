
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
            {name: 'description', type: 'string' },
            {name: 'category', type: 'string' },
            {name: 'guid', type: 'string' },
            {name: 'pubdate', type: 'string' },
        ],
        proxy: new GeoExt.data.ProtocolProxy({
          protocol: new OpenLayers.Protocol.HTTP({
                url: "/hazard/maps.json",
                format: new OpenLayers.Format.GeoJSON({
                 externalProjection: map.displayProjection
                }
                )
            })
        }),
        autoLoad: true
    });
   var love = function() { 
     alert("hi")
   }

     gridPanel = new Ext.grid.GridPanel({
       renderTo: "pdf-grid",
        store: store,
        height: 400,
        columns: [{
          header: "Name",
          width: 250,
          dataIndex: "name"
        },{
          header: "Description",
          width: 350,
          dataIndex: "description"
        },{
          header: "Category",
          width: 250,
          dataIndex: "category"
        },{
          header: "Guid",
          dataIndex: "guid",
          width: 100
        },{
          header: "Publish Date",
          width: 100,
          dataIndex: "pubdate"
          }],
       sm: new GeoExt.grid.FeatureSelectionModel({selectControl: love})
        
    });

    });}
