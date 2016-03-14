Ext.define('mapPanel', {
		extend: 'Ext.panel.Panel',
		alias: 'widget.mapPanel',
        layout: 'fit',
		config:{
			map: null,
            storeLayers: []
		},
		afterRender: function(t, eOpts){
			this.callParent(arguments);
 
			var leafletRef = window.L;
			if (leafletRef == null){
				this.update('No leaflet library loaded');
			} else {
				var map = L.map(this.getId());
				map.setView([21, 15], 3);
				this.setMap(map);
				this.baseLayer = L.tileLayer('https://api.mapbox.com/v4/{mapId}/{z}/{x}/{y}.png?access_token={key}', {
					key: 'pk.eyJ1IjoiY295bGU1MjgwIiwiYSI6ImNpbDRqczl1dzQydDV2Zm0zcjg0cGt5MGMifQ.fLKS-GqFeQOi6Z3pBwvm1Q',
					mapId: "mapbox.satellite",
					maxZoom: 18
				}).addTo(map);
			}
		},
        
        changeBaseLayer: function (baselayerString) {
            console.log("baselayer", baselayerString);
            this.baseLayer.options.mapId = baselayerString;
            this.baseLayer.redraw();
        },

        onResize: function(w, h, oW, oH){
            this.callParent(arguments);
            var map = this.getMap();
            if(map){
                map.invalidateSize();
            }
        },
        
        addMapLayer: function (data, plugin) {
            var map = this.getMap();
            var features = [];
            data.forEach(function (item){
                console.log("addmapLayer data.forEach", item);
                features.push(item.data.feature);    
            });
            var newLayer = L.geoJson(features, {
                onEachFeature: function (feature, layer) {
                    console.log("feature", feature);
                    var description = "";
                    for(i in feature.properties){
                        description += i + ": " + feature.properties[i] + "<br>";
                    }
                    layer.bindPopup(description);
                }
            }).addTo(map);
            this.config.storeLayers.push({name: plugin, layer: newLayer});
        },
        
        addPluginLayerToMap: function (plugin) {
            if(plugin !== 'all'){    
                var me = this;
                var data = [];
                var store = Ext.StoreMgr.lookup(plugin);
                store.each(function (item){
                    console.log("Map Panel Add Feature Store.each", item);
                    data.push(me.correctGeoJsonFeature(item));
                });
                this.addMapLayer(data, plugin);
            }
        },
        //Correct GeoJson Feature: Leaflet maps reverse the LatLong order. This funciton corrects this. 
        correctGeoJsonFeature: function (row) {
            var geoPoints = [];
            JSONfeature = JSON.parse(row.data.feature);
            
            geoPoints[0] = JSONfeature.geometry.coordinates[1];
            geoPoints[1] = JSONfeature.geometry.coordinates[0];
            
            JSONfeature.geometry.coordinates = geoPoints;
            row.data.feature = JSONfeature;
            return row;
        },
        
        displaySelectedPluginLayer: function (plugin) {
            if(plugin !== 'all'){
                
            }
            
        }
    
	});