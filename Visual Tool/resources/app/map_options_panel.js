Ext.define("map_options",{
    extend: "Ext.form.Panel",
    layout: "vbox",
    itemId: "mapOptions",
    title: "Map Options",
    items: [{
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
    }],
    initComponent: function (){
        
        Ext.apply(this, {
			
			});
		this.callParent();
	}
});