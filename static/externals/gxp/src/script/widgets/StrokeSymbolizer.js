/**
 * Copyright (c) 2008-2010 The Open Planning Project
 * 
 * @include widgets/form/ColorField.js
 */

/** api: (define)
 *  module = gxp
 *  class = StrokeSymbolizer
 *  base_link = `Ext.FormPanel <http://extjs.com/deploy/dev/docs/?class=Ext.FormPanel>`_
 */
Ext.namespace("gxp");

/** api: constructor
 *  .. class:: StrokeSymbolizer(config)
 *   
 *      Form for configuring a symbolizer stroke.
 */
gxp.StrokeSymbolizer = Ext.extend(Ext.FormPanel, {
    
    /** api: config[symbolizer]
     *  ``Object``
     *  A symbolizer object that will be used to fill in form values.
     *  This object will be modified when values change.  Clone first if
     *  you do not want your symbolizer modified.
     */
    symbolizer: null,
    
    /** api: config[defaultSymbolizer]
     *  ``Object``
     *  Default symbolizer properties to be used where none provided.
     */
    defaultSymbolizer: null,
    
    /** api: config[colorManager]
     *  ``Function``
     *  Optional color manager constructor to be used as a plugin for the color
     *  field.
     */
    colorManager: null,
    
    /** api: config[dashStyles]
     *  ``Array(Array)``
     *  A list of [value, name] pairs for stroke dash styles.
     *  The first item in each list is the value and the second is the
     *  display name.  Default is [["solid", "solid"], ["2 4", "dash"],
     *  ["1 4", "dot"]].
     */
    dashStyles: [["solid", "solid"], ["4 4", "dash"], ["2 4", "dot"]],
    
    border: false,
    
    initComponent: function() {
        
        if(!this.symbolizer) {
            this.symbolizer = {};
        }        
        Ext.applyIf(this.symbolizer, this.defaultSymbolizer);

        var colorFieldPlugins;
        if (this.colorManager) {
            colorFieldPlugins = [new this.colorManager];
        }

        this.items = [{
            xtype: "fieldset",
            title: "Stroke",
            autoHeight: true,
            defaults: {
                width: 100 // TODO: move to css
            },
            items: [{
                xtype: "combo",
                name: "style",
                fieldLabel: "Style",
                store: new Ext.data.SimpleStore({
                    data: this.dashStyles,
                    fields: ["value", "display"]
                }),
                displayField: "display",
                valueField: "value",
                value: this.getDashArray(this.symbolizer["strokeDashstyle"]) || "solid",
                mode: "local",
                allowBlank: true,
                triggerAction: "all",
                editable: false,
                listeners: {
                    select: function(combo, record) {
                        this.symbolizer["strokeDashstyle"] = record.get("value");
                        this.fireEvent("change", this.symbolizer);
                    },
                    scope: this
                }
            }, {
                xtype: "gx_colorfield",
                name: "color",
                fieldLabel: "Color",
                value: this.symbolizer["strokeColor"],
                plugins: colorFieldPlugins,
                listeners: {
                    valid: function(field) {
                        this.symbolizer["strokeColor"] = field.getValue();
                        this.fireEvent("change", this.symbolizer);
                    },
                    scope: this
                }
            }, {
                xtype: "textfield",
                name: "width",
                fieldLabel: "Width",
                value: this.symbolizer["strokeWidth"],
                listeners: {
                    change: function(field, value) {
                        this.symbolizer["strokeWidth"] = value;
                        this.fireEvent("change", this.symbolizer);
                    },
                    scope: this
                }
            }, {
                xtype: "slider",
                name: "opacity",
                fieldLabel: "Opacity",
                values: [(this.symbolizer["strokeOpacity"] == null) ? 100 : this.symbolizer["strokeOpacity"] * 100],
                isFormField: true,
                listeners: {
                    changecomplete: function(slider, value) {
                        this.symbolizer["strokeOpacity"] = value / 100;
                        this.fireEvent("change", this.symbolizer);
                    },
                    scope: this
                },
                plugins: [
                    new GeoExt.SliderTip({
                        getText: function(slider) {
                            return slider.getValue() + "%";
                        }
                    })
                ]
            }]
        }];

        this.addEvents(
            /**
             * Event: change
             * Fires before any field blurs if the field value has changed.
             *
             * Listener arguments:
             * symbolizer - {Object} A symbolizer with stroke related properties
             *     updated.
             */
            "change"
        ); 
 
        gxp.StrokeSymbolizer.superclass.initComponent.call(this);
        
    },

    getDashArray: function(style) {
        var array;
        if (style) {
            var parts = style.split(/\s+/);
            var ratio = parts[0] / parts[1];
            var array;
            if (!isNaN(ratio)) {
                array = ratio >= 1 ? "4 4" : "2 4"
            }
        }
        return array;
    }
    
    
    
});

/** api: xtype = gx_strokesymbolizer */
Ext.reg('gx_strokesymbolizer', gxp.StrokeSymbolizer); 
