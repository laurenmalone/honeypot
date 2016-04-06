Ext.define('CartoDBComponent', {
	extend: 'Ext.Component',
	alias: 'widget.cartodbcomponent',
	config: {
		map: null,
		cartodb: null
	},

	panTo: function(lat, lng, zoom) {
		this.map.setView([lat,lng], 10);
	},

	setBaseLayer: function(layer) {
		if (this.baseLayer) {
			this.map.removeLayer(this.baseLayer);
		}
		this.baseLayer = L.tileLayer(layer.url, {
			attribution: layer.attribution,
			tms: (layer.tms) ? layer.tms : false
		});
		this.baseLayer.addTo(this.map).bringToBack();
		
	},

	afterRender: function(t, eOpts){
		this.callParent(arguments);
		var me = this;
		var leafletRef = window.L;
		if (leafletRef == null){
			this.update('No leaflet library loaded.');
		} else {
			me.leafletMap = L.map(this.getId(), {
               minZoom: 2,
			   maxZoom: 19,
			   attributionControl: true
			});
            
			me.leafletMap.setView([21,15], 3);
			this.setMap(me.leafletMap);
		}
	},

	onResize: function(w, h, oW, oH){
		this.callParent(arguments);
		var map = this.getMap();
		if(map){
			map.invalidateSize();
		}
	}

});
