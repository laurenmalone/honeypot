Ext.define('mapPanel', {
		extend: 'Ext.panel.Panel',
		alias: 'widget.mapPanel',
        layout: 'fit',
		config:{
			map: null,
            storeLayers: []
		},
		/**
		 * @param  {any} t
		 * @param  {any} eOpts
		 */
		afterRender: function(t, eOpts){
			this.callParent(arguments);
            
			var leafletRef = window.L;
			if (leafletRef == null){
				this.update('No leaflet library loaded');
			} else {
				var map = L.map(this.getId());
				map.setView([21, 15], 3);
                map.options.maxZoom = 18;
				this.setMap(map);
                map.setMaxBounds([[84.67351256610522, -180.0234375], [-58.995311187950925, 215.2421875]]);
				this.baseLayer = L.tileLayer('https://api.mapbox.com/v4/{mapId}/{z}/{x}/{y}.png?access_token={key}', {
					key: 'pk.eyJ1IjoiY295bGU1MjgwIiwiYSI6ImNpbDRqczl1dzQydDV2Zm0zcjg0cGt5MGMifQ.fLKS-GqFeQOi6Z3pBwvm1Q',
					mapId: "mapbox.satellite",
					maxZoom: 18,
                    minZoom: 3,
                    continuousWorld: true
                    
				}).addTo(map);
			}
		},
        
        /**
         * @param  {any} baselayerString
         */
        changeBaseLayer: function (baselayerString) {
//            console.log("baselayer", baselayerString);
            this.baseLayer.options.mapId = baselayerString;
            this.baseLayer.redraw();
        },
        /**
         * @param  {any} w
         * @param  {any} h
         * @param  {any} oW
         * @param  {any} oH
         */
        onResize: function(w, h, oW, oH){
            this.callParent(arguments);
            var map = this.getMap();
            if(map){
                map.invalidateSize();
            }
        },
        
        /**
         * @param  {any} data
         * @param  {any} plugin
         */
        addMapLayer: function (data, plugin) {
            var map = this.getMap();
            var features = [];
            var markerList = [];
            var markers = L.markerClusterGroup({ chunkedLoading: true});
                
            // data.forEach(function (item){
            //     if(item.data && item.data.ip_address && item.data.feature){
            //         //console.log("addmapLayer data.forEach", item);
            //         item.data.feature.properties.ip_address = item.data.ip_address;
            //         features.push(item.data.feature);
            //     }

                        
            // });
            data.forEach(function (item) {
                if(item.data && item.data.ip_address && item.data.feature){
                    var address = item.data.feature.geometry.coordinates;
                    item.data.feature.properties.ip_address = item.data.ip_address;
                    var title = "";
                    for(var key in item.data.feature.properties){
                        title += key + ": " + item.data.feature.properties[key] + "<br>";
                    }
                    var marker = L.marker(L.latLng(address[0], address[1]), {title: title});
                    marker.bindPopup(title);
                    markerList.push(marker);  
                }
                
            });
            
            /**
             * @param  {any} features
             */
//             var newLayer = L.geoJson(features, {
//                 onEachFeature: function (feature, layer) {
// //                    console.log("feature", feature);
//                     var description = "";
//                     for(i in feature.properties){
//                         if(feature.properties[i]){
//                             description += i + ": " + feature.properties[i] + "<br>";    
//                         }
                        
//                     }
//                     description += "plugin name: " + plugin;
//                     layer.bindPopup(description);
//                 }
//             }).addTo(map);
            // this.config.storeLayers.push({name: plugin, layer: newLayer}); 
            
            markers.addLayers(markerList);
            map.addLayer(markers);
            this.config.storeLayers.push({name: plugin, layer: markers});       
    
        },
        /**
         * @param  {any} data
         * @param  {any} plugin
         */
        addPluginLayerToMap: function (plugin) {
            if(plugin !== 'all'){    
                var me = this;
                var correctedData = [];
                var store = Ext.StoreMgr.lookup(plugin + "features");
                store.each(function (item){
                    //console.log("Map Panel Add Feature Store.each", item);
                    // correctedData.push(me.correctGeoJsonFeature(item));
                    correctedData.push(me.correctGeoJsonFeature(item));
                });
                this.addMapLayer(correctedData, plugin);
            }
        },
        //Correct GeoJson Feature: Leaflet maps reverse the LatLong order. This funciton corrects this. 
        /**
         * @param  {any} item
         */
        correctGeoJsonFeature: function (item) {
            if(item.data.feature){    
                var geoPoints = [];
                JSONfeature = JSON.parse(item.data.feature);

                // geoPoints[0] = JSONfeature.geometry.coordinates[1];
                // geoPoints[1] = JSONfeature.geometry.coordinates[0];
                
                geoPoints[1] = JSONfeature.geometry.coordinates[1];
                geoPoints[0] = JSONfeature.geometry.coordinates[0];

                JSONfeature.geometry.coordinates = geoPoints;
                item.data.feature = JSONfeature;
            }
            
            return item;
        },
        
        /**
         * @param  {any} plugin
         */
        displaySelectedPluginLayer: function (plugin) {
            var map = this.getMap();
            if(plugin !== 'all'){
                this.config.storeLayers.forEach(function (item){
                    if(item.name === plugin) {
                        map.addLayer(item.layer);    
                    }else{
                        map.removeLayer(item.layer);
                    }   
                });
            }else{
                this.config.storeLayers.forEach(function (item){
                    map.addLayer(item.layer);
                });
            }
            
        }
    
	});