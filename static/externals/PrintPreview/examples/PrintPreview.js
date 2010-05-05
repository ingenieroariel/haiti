var mapPanel, printMapPanel, legendPanel;

Ext.onReady(function() {

    mapPanel = new GeoExt.MapPanel({
        region: "center",
        layers: [
            new OpenLayers.Layer.WMS("Tasmania State Boundaries",
                "http://demo.opengeo.org/geoserver/wms",
                {layers: "topp:tasmania_state_boundaries"}, {singleTile: true}),
            new OpenLayers.Layer.WMS("Tasmania Water Bodies",
                "http://demo.opengeo.org/geoserver/wms",
                {layers: "topp:tasmania_water_bodies", transparent: true},
                {buffer: 0})],
        center: [146.56, -41.7],
        zoom: 6,
        bbar: [{
            text: "Print...",
            handler: showPrintWindow
        }]
    });

    legendPanel = new GeoExt.LegendPanel({
        width: 200,
        region: "west",
        defaults: {
            style: "padding:5px",
            imageFormat: "image/png"
        }
    });
    new Ext.Panel({
        layout: "border",
        renderTo: "content",
        width: 800,
        height: 350,
        items: [mapPanel, legendPanel]
    });    
});

function showPrintWindow() {
    var printWindow = new Ext.Window({
        title: "Print",
        modal: true,
        border: false,
        resizable: false,
        width: 360,
        items: new GeoExt.ux.PrintPreview({
            printProvider: {
                // using get for remote service access without same origin
                // restriction. For async requests, we would set method to "POST".
                method: "GET",
                //method: "POST",
                
                // capabilities from script tag in Printing.html.
                capabilities: printCapabilities,
                listeners: {
                    "print": function() {printWindow.close();}
                }
            },
            includeLegend: true,
            mapTitle: "PrintMapPanel Demo",
            sourceMap: mapPanel,
            legend: legendPanel
        })
    }).show().center();
}
