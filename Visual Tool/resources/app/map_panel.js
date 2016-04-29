Ext.define('mapPanel', {
		extend: 'Ext.panel.Panel',
		alias: 'widget.mapPanel',
        layout: 'fit',
		config:{
			map: null,
            storeLayers: []
		},
		/**
         * This method is called after the mapPanel is finished being renderd.
         * It will set the base tile map and options
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
         * This method changes the base map tile Layer 
         * @param  {string} baselayerString
         */
        changeBaseLayer: function (baselayerString) {
            this.baseLayer.options.mapId = baselayerString;
            this.baseLayer.redraw();
        },
        /**
         * This method will resize the map based on the size of the container and 
         * will adjust accordingly
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
         * This method adds an indiviual layer to the map and then adds the name and reference in
         * the config.storelayers array
         * @param  {object} data
         * @param  {string} plugin
         */
        addMapLayer: function (data, plugin) {
            var map = this.getMap();
            var features = [];
            var markerList = [];
            var markers = L.markerClusterGroup({ chunkedLoading: true});
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
            markers.addLayers(markerList);
            map.addLayer(markers);
            this.config.storeLayers.push({name: plugin, layer: markers});       
        },
        /**
         * This method is called from the app controller.  It calls the correctGeoJsonFeature method
         * and then calls the addMapLayer function.  
         * @param  {string} plugin
         */
        addPluginLayerToMap: function (plugin) {
            if(plugin !== 'all'){    
                var me = this;
                var correctedData = [];
                var store = Ext.StoreMgr.lookup(plugin + "features");
                store.each(function (item){
                    correctedData.push(me.correctGeoJsonFeature(item));
                });
                this.addMapLayer(correctedData, plugin);
            }
        },
        /**
         * This method will correct the GeoJasonFeature and convert it into
         * an object instead of a string 
         * @param  {object} item
         */
        correctGeoJsonFeature: function (item) {
            if(item.data.feature){    
                var geoPoints = [];
                JSONfeature = JSON.parse(item.data.feature);
                item.data.feature = JSONfeature;
            }
            return item;
        },
        /**
         * This function will hide or show layers based on user input.  The all layer is not an indiviual 
         * layer but the combination of all layers an once.
         * @param  {string} plugin
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