Ext.onReady(function () {
	//url: './resources/app/jsons/testFeature.json'
    
    west_menu = Ext.create("menu_panel",{
        listeners: {
            afterrender: function (){
                west_menu.setView(0);
            }
        }
    });
    
    this.pluginsArray = [];
    pluginsStore = {};
    var ormString = JSON.stringify({
                        "fields": [{
                            "name": "area_code",
                            "type": "string"
                        }, {
                            "name": "city",
                            "type": "string"
                        }]
                    });
    console.log("ormString", ormString);
    var jsonFromString = JSON.parse(ormString);
    console.log("fromString", jsonFromString.fields);
    
    
    
    var loadPlugins = function () {
        pluginsStore = Ext.create('Ext.data.Store', {
            storeId: "plugins",
            fields: [{name: 'value', type: "string"}, 
                     {name: 'display', type: "string"}, 
                     {name: 'orm', type: "string"}
                     ],
            proxy: {
                type: 'jsonp',
                url: './resources/app/jsons/plugins.json',
                reader: {
                    type: 'json',
                    rootProperty: 'rows'
                }
            },
            autoLoad: false
        });
        return pluginsStore;
    };
    
    var setupPluginStores = function () {
        var me = this;
        pluginsStore = loadPlugins();
        pluginsStore.load(function(records, operation, success){
            var pluginCombo = west_menu.down("#pluginCombo");
            pluginCombo.bindStore(pluginsStore);
            pluginCombo.setValue('All');
            var pluginComboTable = west_menu.down("#pluginComboTable")
            pluginComboTable.bindStore(pluginsStore);
            pluginComboTable.setValue('All');
            var pluginComboAna = west_menu.down("#pluginComboAnalytics");
            pluginComboAna.bindStore(pluginsStore);
            pluginComboAna.setValue('All');
            me.pluginsStore.each(function(item){
                console.log("store item", item);
                createPluginStore(item);
            });
        });
    };
    
    var createPluginStore = function (plugin) {
        plugin.data.fields = (plugin.data.orm) ? JSON.parse(plugin.data.orm) : "";
        if(plugin.data.value === "all"){
            center_panel.grid_panel.setStoreColumns(plugin.data.fields.fields, plugin.data.value);
        }
        singlePluginStore = Ext.create('Ext.data.Store', {
            storeId: plugin.data.value,
            proxy: {
                type: 'jsonp',
                url: './resources/app/jsons/' + plugin.data.value + ".json",
                reader: {
                    type: 'json',
                    rootProperty: 'rows'
                }
            },
            autoLoad: false
        });
        pluginsArray.push(singlePluginStore);
        singlePluginStore.load({scope: this, callback: function (records, operation, success){
                console.log("records", records, operation);
                
            }
        });
        
    };
    
    setupPluginStores();
    
    center_panel = Ext.create("center_panel");
        
    west_menu.down("#pluginComboTable").on('select', function(combo, records, eOpts){
        center_panel.grid_panel.setStoreColumns(records.data.fields.fields, records.data.value);
    });
    
    
    west_menu.down("#map_table_button").on('change', function(segGroup, newValue, oldValue){
        console.log(newValue[0]);
        if(newValue[0] == 1){
//            Ext.getStore('table_data_store').load();
        }
        center_panel.setView(newValue[0]);
        west_menu.setView(newValue[0]);
    });
    
    west_menu.down("#baseLayerCombo").on('select', function(combo, records, eOpts){
        center_panel.map_panel.changeBaseLayer(records.data.value); 
    });
    
    west_menu.down("#pluginCombo").on('select', function(combo, records, eOpts){
        center_panel.map_panel.showPluginLayer(records.data.value); 
    });
    
    
    center_panel.getLayout().setActiveItem(0);
//    west_menu.getLayout().setActiveItem(0);
	Ext.create('Ext.Viewport', {
		title: 'Honey Pot',
		layout: 'border',
		items: [center_panel,west_menu]

	});
});
