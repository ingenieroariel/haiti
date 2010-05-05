/** api: (define)
 *  module = GeoExplorer
 *  class = Embed
 *  base_link = GeoExplorer
 */

/** api: constructor
 *  ..class:: GeoExplorer.Embed(config)
 *
 *  Create a GeoExplorer application suitable for embedding in larger pages.
 */
Embed = Ext.extend(GeoExplorer, {

    zoomLevelText: "UT:Zoom Level: {zoom}",

    useToolbar: true,

    /**
     * api: method[createLayout]
     * Create the various parts that compose the layout.
     */
    createLayout: function() {
        // create the map
        // TODO: check this.initialConfig.map for any map options
        this.map = new OpenLayers.Map({
            allOverlays: true,
            projection: new OpenLayers.Projection("EPSG:900913"),
            displayProjection: new OpenLayers.Projection("EPSG:4326"),
            units: "m",
            maxResolution: 156543.0339,
            maxExtent: new OpenLayers.Bounds(
                -20037508.34, -20037508.34,
                 20037508.34,  20037508.34
            ),
            controls: [
                new OpenLayers.Control.PanPanel(),
                new OpenLayers.Control.ZoomPanel()
            ]
        });

        //** Remove this code when OpenLayers #2069 is closed **
        var onDoubleClick = function(ctrl, evt) { 
 	        OpenLayers.Event.stop(evt ? evt : window.event); 
        };
        var controls = this.map.controls[0].controls;
        for(var i = 0; i < controls.length; i++){
            OpenLayers.Event.observe(controls[i].panel_div, "dblclick",  
 	                             OpenLayers.Function.bind(onDoubleClick, this.map.controls[0], controls[i])); 
        }        
        //******************************************************

        //TODO: make this more configurable
        this.map.events.on({
            "preaddlayer" : function(evt){
                if(evt.layer.mergeNewParams){
                    var maxExtent = evt.layer.maxExtent;
                    if (maxExtent) evt.layer.mergeNewParams({
                        transparent: true,
                        format: "image/png",
                        tiled: true,
                        tilesorigin: [maxExtent.left, maxExtent.bottom]
                    });
                }
            },
            scope : this
        });
        

        // place map in panel
        var mapConfig = this.initialConfig.map || {};
        var center = mapConfig.center && 
            new OpenLayers.LonLat(mapConfig.center[0], mapConfig.center[1]).transform(
                new OpenLayers.Projection("EPSG:4326"),
                new OpenLayers.Projection("EPSG:900913")
            ); 
        this.mapPanel = new GeoExt.MapPanel({
            layout: "anchor",
            border: true,
            region: "center",
            map: this.map,
            // TODO: update the OpenLayers.Map constructor to accept an initial center
            center: center,
            // TODO: update the OpenLayers.Map constructor to accept an initial zoom
            zoom: mapConfig.zoom,
            items: [
                {
                    xtype: "gx_zoomslider",
                    vertical: true,
                    height: 100,
                    plugins: new GeoExt.ZoomSliderTip({
                        template: "<div>"+this.zoomLevelText+"</div>"
                    })
                }
            ]
        });
        this.mapPanel.add(this.createMapOverlay());
        
        // create layer store
        this.layers = this.mapPanel.layers;
        
        var toolbar;
        if (this.useToolbar) {
            toolbar = new Ext.Toolbar({
                xtype: "toolbar",
                region: "north",
                disabled: true,
                items: this.createTools()
            });

            this.on("ready", function() {
                toolbar.enable();
            });
        }

        this.mapPanel.map.addControl(new OpenLayers.Control.Navigation());

        var viewportConfig = Ext.applyIf({
                layout: "fit",
                hideBorders: true,
                tbar: toolbar,
                items: {
                    layout: "border",
                    deferredRender: false,
                    items: [this.mapPanel]
                }
            }, this.view
        );

        var viewport = new this.view.type(viewportConfig);
    }
});
