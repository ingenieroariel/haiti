/**
 * Copyright (c) 2009 The Open Planning Project
 * 
 * Published under the BSD license.
 * See http://svn.opengeo.org/gxp/trunk/license.txt for the full text
 * of the license.
 */

Ext.onReady(function() {
    
    // create a new WMS capabilities store
    var store = new GeoExt.data.WMSCapabilitiesStore({
        url: "/geoserver/wms?request=GetCapabilities"
    });
    store.load();

    // create a grid to display records from the store
    var grid = new Ext.grid.GridPanel({
        title: "WMS Capabilities",
        store: store,
        cm: new Ext.grid.ColumnModel([
            {header: "Name", dataIndex: "name", sortable: true},
            {id: "title", header: "Title", dataIndex: "title", sortable: true}
        ]),
        sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
        autoExpandColumn: "title",
        renderTo: "capgrid",
        height: 300,
        width: 310,
        bbar: ["->", {
            text: "Add Layer",
            handler: function() {
                var record = grid.getSelectionModel().getSelected();
                if(record) {
                    var copy = record.clone();
                    copy.get("layer").mergeNewParams({
                        format: "image/png",
                        transparent: "true"
                    });
                    mapPanel.layers.add(copy);
                    mapPanel.map.zoomToExtent(
                        OpenLayers.Bounds.fromArray(copy.get("llbbox"))
                    );
                }
            }
        }]
    });
    
    // create a map panel
    var mapPanel = new GeoExt.MapPanel({
        renderTo: "mappanel",
        width: 350,
        height: 300
    });
    
    var tree = new Ext.tree.TreePanel({
        title: "Layers",
        renderTo: "tree",
        root: new GeoExt.tree.LayerContainer({
            text: 'Map Layers',
            layerStore: mapPanel.layers,
            leaf: false,
            expanded: true
        }),
        enableDD: true,
        width: 250,
        height: 300,
        tbar: [{
            text: "Show Properties",
            handler: function() {
                var node = tree.getSelectionModel().getSelectedNode();
                var record;
                if(node && node.layer) {
                    var layer = node.layer;
                    var store = node.layerStore;
                    record = store.getAt(store.findBy(function(record) {
                        return record.get("layer") === layer;
                    }));
                }
                if(record) {
                    showProp(record);
                }
            }
        }]
    });
    

});

var prop;
function showProp(record) {
    if(prop) {
        prop.close();
    }
    prop = new Ext.Window({
        title: "Properties: " + record.get("title"),
        width: 280,
        height: 350,
        layout: "fit",
        items: [{
            xtype: "gx_wmslayerpanel",
            layerRecord: record,
            defaults: {style: "padding: 10px"}
        }]
    });
    prop.items.get(0).add(new gxp.WMSStylesDialog({
        title: "Styles",
        layerRecord: record,
        autoScroll: true
    }));
    prop.show();
}
