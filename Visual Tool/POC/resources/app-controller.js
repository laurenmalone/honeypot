Ext.onReady(function () {
	//url: './resources/app/jsons/testFeature.json'
    
    west_menu = Ext.create("menu_panel",{
        listeners: {
            afterrender: function (){
                west_menu.setView(0);
            }
        }
    });
    center_panel = Ext.create("center_panel");
    this.pluginsArray = [];
    pluginsStore = {};
    
    

    var loadPlugins = function () {
        pluginsStore = Ext.create('Ext.data.Store', {
            storeId: "plugins",
            fields: [{name: 'value', type: "string"}, 
                     {name: 'display', type: "string"}, 
                     {name: 'orm', type: "string"}
                     ],
            proxy: {
                type: 'jsonp',
                url: CONFIG.url + '/',
                reader: {
                    type: 'json',
                    rootProperty: 'rows'
                },
                listeners: {
                    exception: function(proxy, response, operation) {
                        
                        var message = "There was an error connecting to the Honey Pot Http server</br> @" + CONFIG.url
                        console.log("loading error", operation);
                        Ext.create('widget.uxNotification', {
											title: 'Error Connecting to Server',
											position: 't',
											manager: 'Error',
                                            width: "35%",
                                            autoClose: false,
											spacing: 20,
											html: message
										}).show();
                    }
                }
            },
            autoLoad: false
        });
        return pluginsStore;
    };
    
    
    var createAllStore = function () {
        Ext.create('Ext.data.Store', {
            storeId: "all",
            fields: [{name: 'plugin', type: "string"}, 
                     {name: 'hits', type: "integer"}
                     ],
            proxy: {
                type: 'jsonp',
                url: CONFIG.url + '/plugins',
                reader: {
                    type: 'json',
                    rootProperty: 'rows'
                }
            },
            autoLoad: true
        });
    };
    
    var setupPluginStores = function () {
        var me = this;
        var pluginsStore = loadPlugins();
        pluginsStore.load(function(records, operation, success){
            var pluginCombo = center_panel.down("#pluginCombo");
            pluginCombo.bindStore(pluginsStore);
            pluginCombo.setValue('All');
            var pluginComboTable = center_panel.down("#pluginComboTable");
            pluginComboTable.bindStore(pluginsStore);
            pluginComboTable.setValue('All');
            var pluginComboAna = center_panel.down("#pluginComboAnalytics");
            pluginComboAna.bindStore(pluginsStore);
            pluginComboAna.setValue('All');
            createAllStore();
//            center_panel.grid_panel.setStoreColumns(["plugin", 'hits'], 'all');
            me.pluginsStore.each(function(item){
                console.log("store item", item);
                createPluginStore(item);
            });
            pluginsStore.add(
                {
                    value: 'all', 
                    display: 'All', 
                    orm: '{"fields":[{"name":"Plugin","type":"string"},{"name":"Hits","type":"integer"}]}',
                    fields: {
                        fields: [
                            {name: 'Plugins', type: "string"},{name: "Hits", type: "integer"}
                        ]
                    } 
                }
            );
            center_panel.grid_panel.setStoreColumns([{name: 'Plugins', type: "string"},{name: "Hits", type: "integer"}], 'all');
                    // Remove Loading Div
            Ext.get('loading').remove();
            Ext.get('loading-mask').fadeOut({
                remove: true
            });
        });
    };
    
    var createPluginStore = function (plugin) {
        plugin.data.fields = (plugin.data.orm) ? JSON.parse(plugin.data.orm) : "";
        singlePluginStore = Ext.create('Ext.data.Store', {
            storeId: plugin.data.value,
            proxy: {
                type: 'jsonp',
                url: CONFIG.url + "/plugins/" + plugin.data.value + "",
                reader: {
                    type: 'json',
                    rootProperty: 'rows'
                },
                listeners: {
                    exception: function(proxy, response, operation) {
                        
                        var message = "There was an error loading data for plugin " + plugin.data.value + "</br> @URL " + CONFIG.url
                        console.log("loading error", operation);
                        Ext.create('widget.uxNotification', {
											title: 'Error Connecting to Server',
											position: 't',
											manager: 'Error',
                                            width: "35%",
                                            autoClose: false,
											spacing: 20,
											html: message
										}).show();
                    }
                }
            },
            autoLoad: false
        });
        pluginsArray.push(singlePluginStore);
        singlePluginStore.load({scope: this, callback: function (records, operation, success){
                console.log("records", records, operation);
                center_panel.map_panel.addPluginLayerToMap(plugin.data.value); 
            }
        });
        
    };
    
    var continuousUpdate = function (updateTime) {
        var timer = updateTime*1000;
        while(this.continuousFlag){
          setTimeout(function(){
            
          }, timer);
      }  
    };
    
    setupPluginStores();
    
    
        
    center_panel.down("#pluginComboTable").on('select', function(combo, records, eOpts){
        center_panel.grid_panel.setStoreColumns(records.data.fields.table.column, records.data.value);
        console.log("");
    });
    
    
    center_panel.down("#map_table_button").on('change', function(segGroup, newValue, oldValue){
        console.log(newValue[0]);
//        if(newValue[0] == 1){
////            Ext.getStore('table_data_store').load();
//        }
        center_panel.setView(newValue[0]);
        switch(newValue[0]){
            case 0:
                center_panel.down("#baseLayerCombo").show();
                center_panel.down("#pluginCombo").show();
                center_panel.down("#pluginComboTable").hide();
                center_panel.down("#pluginComboAnalytics").hide();
                break;
            case 1:
                center_panel.down("#pluginComboTable").show();
                center_panel.down("#pluginCombo").hide();
                center_panel.down("#baseLayerCombo").hide();
                center_panel.down("#pluginComboAnalytics").hide();
                break;
            case 2: 
                center_panel.down("#pluginComboAnalytics").show();
                center_panel.down("#pluginCombo").hide();
                center_panel.down("#baseLayerCombo").hide();
                center_panel.down("#pluginComboTable").hide();
                break;
            default:
                console.log("ERROR");
        }
//            center_panel.down("#")
//        west_menu.setView(newValue[0]);
    });
    
    center_panel.down("#baseLayerCombo").on('select', function(combo, records, eOpts){
        center_panel.map_panel.changeBaseLayer(records.data.value); 
    });
    
    center_panel.down("#pluginCombo").on('select', function(combo, records, eOpts){
        
    });
    
    
    center_panel.getLayout().setActiveItem(0);
//    west_menu.getLayout().setActiveItem(0);
	Ext.create('Ext.Viewport', {
		title: 'Honey Pot',
		layout: 'border',
		items: [center_panel]

	});
    

    
});
