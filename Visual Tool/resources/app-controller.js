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
//                        console.log("loading error", operation);
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
	
	
	/**
	 */
	var createAllStore = function () {
		var allStore = Ext.create('Ext.data.Store', {
			pageSize: 100,
			storeId: "all",
			fields: [{name: 'plugin', type: "string"}, 
					 {name: 'hits', type: "integer"}
					 ],
			proxy: {
				type: 'jsonp',
				url: CONFIG.url + '/plugins',
				reader: {
					type: 'json',
					rootProperty: 'rows',
                    totalProperty: 'totalCount'
				}
			},
			autoLoad: false
		});
		return allStore;
	};
	
	/**
	 */
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
			var allStore = createAllStore();
//            center_panel.grid_panel.setStoreColumns(["plugin", 'hits'], 'all');
			me.pluginsStore.each(function(item){
//                console.log("store item", item);
				createPluginStore(item);
				loadFeatureStores(item);
			});
			pluginsStore.add(
				{
					value: 'all', 
					display: 'All', 
					orm: '{"fields":[{"name":"table","type":"string"},{"name":"count","type":"integer"}]}',
					fields: {
						table: {
							column: [
								{name: 'table', type: "string"},{name: "count", type: "integer"}
							]
						}
					} 
				}
			);
			center_panel.grid_details_panel.grid_panel.setStoreColumns([{name: 'table', type: "string"},{name: "count", type: "integer"}], 'all');
			allStore.load(function(){
				createPieStore();
				createLineGraphStores(); 
			});
			Ext.get('loading').remove();
			Ext.get('loading-mask').fadeOut({
				remove: true
			});
		});
	};
	
	/**
	 * Create a data store for a plugin. Also calls createLineGraphStores 
	 * @param  {string} plugin
	 */
	var createPluginStore = function (plugin) {
		plugin.data.fields = (plugin.data.orm) ? JSON.parse(plugin.data.orm) : "";
		singlePluginStore = Ext.create('Ext.data.Store', {
			pageSize: 100,
			storeId: plugin.data.value,
			proxy: {
				type: 'jsonp',
				url: CONFIG.url + "/plugins/" + plugin.data.value + "",
				reader: {
					type: 'json',
					rootProperty: 'rows',
                    totalProperty: 'totalCount'
				},
				listeners: {
					exception: function(proxy, response, operation) {
						var message = "There was an error loading data for plugin " + plugin.data.value + "</br> @URL " + CONFIG.url
//                        console.log("loading error", operation);
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
	};
	
	
	/**
	 * @param  {any} plugin
	 */
	function loadFeatureStores(plugin) {
		singleFeatureStore = Ext.create('Ext.data.Store', {
			storeId: plugin.data.value + "features",
			proxy: {
				type: 'jsonp',
				url: CONFIG.url + "/plugins/" + plugin.data.value + "/" + "features",
				reader: {
					type: 'json',
					rootProperty: 'rows'
				},
				listeners: {
					exception: function(proxy, response, operation) {
						var message = "There was an error loading data for plugin " + plugin.data.value + "</br> @URL " + CONFIG.url
//                        console.log("loading error", operation);
						Ext.create('widget.uxNotification', {
											title: 'Error loading features',
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
		singleFeatureStore.load(function (items) {
			center_panel.map_panel.addPluginLayerToMap(plugin.data.value);		
		})	
	};
	
	
	//TODO This method should only create a single store once the data is loaded.
	/**
	 */
	function createLineGraphStores() {
		var allLineGraphStore = Ext.create('Ext.data.Store', {
										storeId:  "allLineGraphStore",
										fields: [{name: 'day', type: "string"}, 
												 {name: 'data1', type: "int"}]
									});
		var dataAll = [{day: "Sunday", data1: 0},{day: "Monday", data1: 0},{day: "Tuesday", data1: 0},{day: "Wednesday", data1: 0},
						{day: "Thursday", data1: 0},{day: "Friday", data1: 0},{day: "Saturday", data1: 0}];
		var yGraphRange = 0;
		Ext.getStore('all').each(function (pluginItem){
			var lineGraphStore = Ext.create('Ext.data.Store', {
										storeId: pluginItem.data.table + "LineGraphStore",
										fields: [{name: 'day', type: "string"}, 
												 {name: 'data1', type: "int"}],
										proxy: {
											type: 'jsonp',
											url: CONFIG.url + '/plugins/' + pluginItem.data.table + "/weekdata",
											reader: {
												type: 'json',
												rootProperty: 'rows'
											}
										},
										autoLoad: false
									});
				lineGraphStore.load(function (items) {
					lineGraphStore.each(function (item) {
						switch(item.data.day){
							case "Sunday":
								dataAll[0].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[0].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							case "Monday":
								dataAll[1].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[1].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							case "Tuesday":
								dataAll[2].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[2].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							case "Wednesday":
								dataAll[3].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[3].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							case "Thursday":
								dataAll[4].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[4].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							case "Friday":
								dataAll[5].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[5].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							case "Saturday":
								dataAll[6].data1 += item.data.data1;
								yGraphRange = (yGraphRange < dataAll[6].data1) ? dataAll[0].data1 : yGraphRange;
								Ext.ComponentQuery.query('#lineGraph')[0].getAxes()[0].setMaximum(yGraphRange * 1.33);
								break;
							default:
								console.log("DATA ERROR IN LINE GRAPH DATA");
						}
					});	
			});
		}, this);
	 	// yGraphRange = yGraphRange * 1.33;
		allLineGraphStore.loadRawData(dataAll, false);
		Ext.ComponentQuery.query('#lineGraph')[0].bindStore(allLineGraphStore);    
	};
	
	
	/**
	 * @param  {any} updateTime
	 */
	var continuousUpdate = function (updateTime) {
		var timer = updateTime*1000;
		while(this.continuousFlag){
		  setTimeout(function(){
			
		  }, timer);
	  }  
	};
	
	setupPluginStores();
	
	/**
	 */
	function createPieStore() {
		var pieChartStore = Ext.create('Ext.data.Store', {
										storeId: "pieChartStore",
										fields: [{name: 'name', type: "string"}, 
												 {name: 'data1', type: "int"}
												 ]
									});
		var totalCount = 0;
		
		Ext.getStore('all').each(function (item){
			totalCount += item.data.count;
			console.log("totalCount", totalCount);
		}, this);
		//TODO fix this duplicate call to gert all store
		 
		Ext.getStore('all').each(function (item){
			var dataObject = {name: item.data.table, data1: (item.data.count / totalCount)*100};
			console.log("dataObject", dataObject);
			if(dataObject.data1 >= 99){
			   dataObject.data1 = 99 
			}else if (dataObject.data1 <= 1){
			   dataObject.data1 = 1  
			}
			pieChartStore.loadRawData(dataObject, true); 
		}, this);
		pieChartStore.commitChanges();
		Ext.ComponentQuery.query('#pieChart')[0].bindStore(pieChartStore);
		
	}; 
		
	center_panel.down("#pluginComboTable").on('select', function(combo, records, eOpts){
		center_panel.grid_details_panel.grid_panel.setStoreColumns(records.data.fields.table.column, records.data.value);
		var store = Ext.getStore(records.data.value);
		Ext.ComponentQuery.query('#pageBar')[0].bindStore(store);
	});
	
	center_panel.down("#pluginComboAnalytics").on('select', function(combo, records, eOpts){
		center_panel.down("#lineGraph").setLineGraphStore(records.data.value + "LineGraphStore");
	});
    
    center_panel.down("#map_table_button").on('change', function(segGroup, newValue, oldValue){
//        console.log(newValue[0]);
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
//                console.log("ERROR");
		}
//            center_panel.down("#")
//        west_menu.setView(newValue[0]);
	});
	
	center_panel.down("#baseLayerCombo").on('select', function(combo, records, eOpts){
		center_panel.map_panel.changeBaseLayer(records.data.value); 
	});
	
	center_panel.down("#pluginCombo").on('select', function(combo, records, eOpts){
		center_panel.map_panel.displaySelectedPluginLayer(records.data.value);
	});
	
	
	center_panel.getLayout().setActiveItem(0);
	Ext.create('Ext.Viewport', {
		title: 'Honey Pot',
		layout: 'border',
		items: [center_panel]

	});
	

	
});
