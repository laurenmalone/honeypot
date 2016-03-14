Ext.define("center_panel",{
    extend: "Ext.panel.Panel",
    layout: "card",
    region: "center",
    items: [],
    initComponent: function (){
		this.map_panel = Ext.create("mapPanel");
        this.grid_panel = Ext.create("grid_panel");
        this.analytics_panel = Ext.create("analytics_panel");

		Ext.apply(this, {
			items:[this.map_panel, this.grid_panel, this.analytics_panel]
			});
		this.callParent();
	},
    setView: function (setCard) {
        this.getLayout().setActiveItem(setCard);
    },
    tbar: [{
                    xtype: 'segmentedbutton',
                    itemId: 'map_table_button',
                    width: "25%",
                    margin: '10 60 0 60',
                    items: [{
                        text: 'Map',
                        itemId: 'map_toggle',
                        pressed: true
                    }, {
                        text: 'Tables',
                        itemId: 'table_toggle'
                    },{
                        text: 'Analytics',
                        itemId: 'analytics_toggle'
                    }]
                },{
                    xtype: "combobox",
                    itemId: "baseLayerCombo",
                    fieldLabel: "Base Layer",
                    labelAlign: "right",
                    value: "Satellite",
                    margin: "10 0 0 0",
                    displayField: "display",
                    valueFiled: "value",
                    queryMode: 'local',
                    store: Ext.create("Ext.data.Store",{
                        fields: [
                            {name: 'display', type: "string"},
                            {name: 'value', type: "string"}
                        ],
                        data: [
                            {display: "Street", value: "mapbox.streets"},
                            {display: "Light", value: "mapbox.light"},
                            {display: "Dark", value: "mapbox.dark"},
                            {display: "Satellite", value: "mapbox.satellite"},
                            {display: "Streets-Satellite", value: "mapbox.streets-satellite"},
                            {display: "Pirates", value: "mapbox.pirates"},
                            {display: "Wheat Paste", value: "mapbox.wheatpaste"},
                            {display: "Streets-Basic", value: "mapbox.streets-basic"},
                            {display: "Comic", value: "mapbox.comic"}

                        ]
                    })
                },{
                    xtype: "combobox",
                    itemId: "pluginCombo",
                    fieldLabel: "Plugin",
                    labelAlign: "right",
                    margin: "10 0 0 0",
                    displayField: "display",
                    valueFiled: "value",
                    queryMode: 'local',
                    store: Ext.StoreMgr.lookup("plugins")
                },{
                    xtype: "combobox",
                    itemId: "pluginComboTable",
                    fieldLabel: "Plugins",
                    margin: "10 0 0 0",
                    displayField: "display",
                    valueFiled: "value",
                    hidden: true,
                    queryMode: 'local',
                    editable: false,
                    listeners: {
                        afterRender: function(){
                            this.select(0)
                        }
                    }
                },{
                    xtype: "combobox",
                    itemId: "pluginComboAnalytics",
                    margin: "10 0 0 0",
                    fieldLabel: "Plugins",
                    displayField: "display",
                    hidden: true,
                    valueFiled: "value",
                    queryMode: 'local'
                },{
                    xtype:'tbfill'
                },{
                    xtype: 'splitbutton',
                    text: "Refresh",
                    menu: [{
                        text: 'Auto 3 Min'
                    }]
                }]
});