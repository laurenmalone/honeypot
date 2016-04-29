Ext.define("analytics_options",{
    extend: "Ext.form.Panel",
    layout: "vbox",
    itemId: "analyticsOptions",
    title: "Analytics Options",
    items: [{
        xtype: "combobox",
        itemId: "pluginComboAnalytics",
        margin: "10 0 0 0",
        fieldLabel: "Plugins",
        displayField: "display",
        valueFiled: "value",
        queryMode: 'local'
    }]
});