Ext.define("analytics_panel", {
	extend: "Ext.panel.Panel",
	layout: "border",
	initComponent: function () {
		
		var pie = Ext.create("center_piechart", {
			listeners: {
				afterrender: function() {
//                    this.redraw();
				}
			}
		});
		this.items = [
			
			pie,
			
			
			Ext.create("south_linegraph", {
			   region: 'south',
				height: "30%",
				split: true,
				initComponent: function () {
					this.setLineGraphStore = function (storeName) {
						var store = Ext.getStore(storeName);
						var max = 0;
						store.each(function (item) {
							max = (max < item.data.data1) ? item.data.data1 : max;
						});
						maxPlus = max + (max * .33);
						this.getAxes()[0].setMaximum(maxPlus);
						this.bindStore(store);
					}
					this.callParent();  
				}
			}),

			Ext.create("Ext.panel.Panel",{
				region: "west",
				itemId: "detailsPanel",
				layout: "fit",
				header: false,
				width: "30%",
				collapsible: true,
				split: true,
				tpl: [
					
					
				],
				html: '',
				items: []

			})
//            ,
//            Ext.create("Ext.panel.Panel",{
//                region: "east",
//                layout: "fit",
//                width: "30%",
//                header: false,
//                collapsible: true,
//                split: true,
//                html: "east",
//                split: true,
//                items: [] 
//            })
		]
//        this.items = Ext.create("center_piechart");
//        this.items = Ext.create("south_linegraph");
		this.callParent();
	}
});