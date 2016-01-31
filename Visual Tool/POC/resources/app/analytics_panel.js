Ext.define("analytics_panel", {
    extend: "Ext.panel.Panel",
    layout: "border",
    initComponent: function () {
        
        this.items = [Ext.create("Ext.panel.Panel",{
            region: "center",
            layout: "fit",
            items: Ext.create("center_piechart"),
            
            }),
            Ext.create("Ext.panel.Panel",{
                region: "south",
                layout: "fit",
                height: "30%",
                split: true,
                items: Ext.create("south_linegraph"),

            }),

            Ext.create("Ext.panel.Panel",{
                region: "west",
                layout: "fit",
                width: "30%",
                split: true,
                html: "south",
                split: true,
                items: []

            }),
            Ext.create("Ext.panel.Panel",{
                region: "east",
                layout: "fit",
                width: "30%",
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