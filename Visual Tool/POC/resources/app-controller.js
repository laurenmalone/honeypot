Ext.onReady(function(){
	
    center_panel = Ext.create("center_panel");
    west_menu = Ext.create("menu_panel",{
        listeners: {
            afterrender: function(){
                west_menu.setView(0);
            }
        }
    });
    
    west_menu.down("#map_table_button").on('change', function(segGroup, newValue, oldValue){
        console.log(newValue[0]);
        if(newValue[0] == 1){
//            Ext.getStore('table_data_store').load();
        }
        center_panel.setView(newValue[0]);
        west_menu.setView(newValue[0]);
    });
    
    
    
    center_panel.getLayout().setActiveItem(0);
//    west_menu.getLayout().setActiveItem(0);
	Ext.create('Ext.Viewport', {
		title: 'Honey Pot',
		layout: 'border',
		items: [center_panel,west_menu]

	});


});