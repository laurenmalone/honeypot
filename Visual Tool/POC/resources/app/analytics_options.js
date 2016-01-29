Ext.define("analytics_options",{
    extend: "Ext.form.Panel",
    layout: "vbox",
    itemId: "analyticsOptions",
    title: "Analytics Options",
    items: [{
        xtype: "combobox",
        margin: "10 0 0 0",
        fieldLabel: "Plugins",
        displayField: "display",
        valueFiled: "value",
        queryMode: 'local',
        store: Ext.create("Ext.data.Store",{
            fields: ['display', 'value'],
            data: [
                {display: "Pie Charts", value: "pieChart"}
            ]
        })
    }],
    initComponent: function (){
		Ext.apply(this, {
			
			});
		this.callParent();
	}
});