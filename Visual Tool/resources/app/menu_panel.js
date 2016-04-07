Ext.define("menu_panel",{
    extend: "Ext.panel.Panel",
    layout: "card",
    items: [],
    split: true,
    collapsible: true,
    collapseMode: "mini",
    width: "20%",
    title: "Menu Panel",
    region: "west",
    initComponent: function (){
		
        this.map_options_panel = Ext.create("map_options");
        this.menu_panel = Ext.create("table_options");
        this.analytics_panel = Ext.create("analytics_options");
        
        Ext.apply(this, {
            items: [
                this.map_options_panel,
                this.menu_panel,
                this.analytics_panel
            ],
			tbar: [{
                xtype: 'segmentedbutton',
                    itemId: 'map_table_button',
                    width: "100%",
                    margin: '10 60 0 60',
                    items: [{
                        text: 'Map',
                        itemId: 'map_toggle',
                        pressed: true
                    }, {
                        text: 'Tables',
                        itemId: 'table_toggle'
                    },{
                        text: 'Analytics',
                        itemId: 'analytics_toggle'
                    }]
            }]
			});
		this.callParent();
	},
    setView: function (setCard) {
        this.getLayout().setActiveItem(setCard);
    }
});