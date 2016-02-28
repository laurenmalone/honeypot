Ext.define("table_options",{
    extend: "Ext.form.Panel",
    layout: "vbox",
    itemId: "tableOptions",
    title: "Table Options",
    items: [{
        xtype: "combobox",
        itemId: "pluginComboTable",
        fieldLabel: "Plugins",
        margin: "10 0 0 0",
        displayField: "display",
        valueFiled: "value",
        queryMode: 'local',
        editable: false,
        listeners: {
            afterRender: function(){
                this.select(0)
            }
        }
    }],
    initComponent: function (){
		Ext.apply(this, {
			
			});
		this.callParent();
	}
});