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
    }
});