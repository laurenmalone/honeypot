Ext.define("map_options",{
    extend: "Ext.form.Panel",
    layout: "vbox",
    itemId: "mapOptions",
    title: "Map Options",
    items: [{
        xtype: "combobox",
        fieldLabel: "Base Layer",
        margin: "10 0 0 0",
        displayField: "display",
        valueFiled: "value",
        queryMode: 'local',
        store: Ext.create("Ext.data.Store",{
            fields: ['display', 'value'],
            data: [
                {display: "Positron", value: "positron"}
            ]
        })
    }],
    initComponent: function (){
		Ext.apply(this, {
			
			});
		this.callParent();
	}
});