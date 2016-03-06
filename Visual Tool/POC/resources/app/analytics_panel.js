Ext.define("analytics_panel", {
    extend: "Ext.panel.Panel",
    layout: "border",
    initComponent: function () {
        
        this.items = [
            
            
            Ext.create("center_piechart", {
                listeners: {
                    afterrender: function() {
                        this.redraw();
                    }
                }
                                                       
            
            }),
            
            Ext.create("south_linegraph", {
               region: 'south',
                height: "30%",
                split: true
            }),

            Ext.create("Ext.panel.Panel",{
                region: "west",
                layout: "fit",
                header: false,
                width: "30%",
                collapsible: true,
                split: true,
                html: '',
                items: []

            }),
            
            Ext.create("Ext.panel.Panel",{
                region: "east",
                layout: "fit",
                width: "30%",
                header: false,
                collapsible: true,
                split: true,
                html: "east",
                split: true,
                items: [] 
            })
        ]
//        this.items = Ext.create("center_piechart");
//        this.items = Ext.create("south_linegraph");
        this.callParent();
    }
});