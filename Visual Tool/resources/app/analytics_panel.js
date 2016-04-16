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
			})
		]
		this.callParent();
	}
});