
function damage_report(get_census,download_link) { 
  jQuery.noConflict();


  Ext.onReady(function() { 
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
      reports = new OpenLayers.Layer.Vector("Damage Points");
      
      draw = new OpenLayers.Control.DrawFeature(reports,
                                OpenLayers.Handler.Polygon),
      map.addControl(draw); 
      jQuery("#draw-control").click(function() { 
          draw.activate();
      });

      var createReporter =  function(handlerType) {
          return new MyHazard.Reporter(handlerType, {
              eventListeners: {
                  report: report,
                  activate: clearPopup, // I  need to change this
                  deactivate: clearPopup, 
                  scope: this
              }
          });
      };

      function make_table(data) { 
          var html = "<a href=\" "+ download_link + "\">Download PDF</a>" + 
              " <table" + 
              "<tr><td>Grade 4 |</td><td>Grade 5 |</td></tr>" + 
              "<tr><td>" + data[0] + "</td><td>" + data[0] + "</td></tr></table>"; 
          return html
          
      } 
      var report = function(evt) { 
          var geojson = new OpenLayers.Format.GeoJSON();
          var geom = geojson.write(evt.geom.transform( 
              new OpenLayers.Projection("EPSG:900913"), 
              new OpenLayers.Projection("EPSG:4326")
          )); 
          jQuery.post(get_census, {"geom" : geom}, function(data) { 
              jQuery("#damage_results").html("");
              jQuery("#damage_results").append("<div>"+ make_table(data) + "</div>");
          });
      } 
      var clearPopup = function() {
        if (this.popup) {
            this.popup.close();
            delete this.popup;

            var controls = this.mapPanel.map.controls;
            for (var i = 0, len = controls.length; i < len; i++) {
                var c = controls[i];
                if (c.active && c.handler && c.handler.cancel) {
                    c.handler.cancel();
                }
            }
        }
      }; 

      var toolGroup = "toolGroup";
      var tools = [ 
            new GeoExt.Action({
                tooltip: this.navActionTipText,
                iconCls: "icon-pan",
                enableToggle: true,
                pressed: true,
                allowDepress: false,
                control: new OpenLayers.Control.Navigation(),
                map: this.map,
                toggleGroup: toolGroup
            }),
          new GeoExt.Action({
                tooltip: "Make a report based on your selection",
                iconCls: "icon-polygon",
                map: this.map,
                toggleGroup: toolGroup,
                group: toolGroup,
                allowDepress: false,
                map: this.map,
               control: createReporter(OpenLayers.Handler.Polygon)
            })
          ]


      var mapControls = new Ext.Toolbar({
          renderTo: "mapControl",
          width: 100,
          height: 40,
          items: tools
      });
      map.addLayers([layer,reports]);
      var panel =  new GeoExt.MapPanel({
        renderTo: 'map',
        height: 450,
        width: window.outerWith,
        layout: 'fit',
        map: map
      });

      map.setCenter(new OpenLayers.LonLat(-8051914,2104311),10)
      ree = new Ext.tree.TreePanel({
        renderTo: "tree",
        root: new GeoExt.tree.LayerContainer({
            text: 'Map Layers',
            layerStore: panel.layers,
            leaf: false,
            expanded: true
        }),
        enableDD: true,
        width: 170,
        height: 200,
    });
  })  
}

