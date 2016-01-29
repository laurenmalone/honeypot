Ext.define('map_panel', {
	extend: 'CartoDBPanel',
	itemId: 'map_panel',
	border: false,
	initComponent: function () {
            this.sql = new cartodb.SQL({
                user: 'crestonedigital',
                format: 'geojson'
            });

		this.baselayer = {
			positron: {
				url: 'http://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png',
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
			}
		}
		

		this.callParent();
	},

	changeBaseMap: function (layer) {
		this.mapComponent.setBaseLayer(this.baselayer[layer]);
	},

	afterRender: function () {
		var me = this;
		setTimeout(function () {
			console.log(me.baselayer.positron);
			me.mapComponent.setBaseLayer(me.baselayer.positron);
//            cartodb.createLayer(me.mapComponent.leafletMap, 'https://crestonedigital.cartodb.com/api/v2/viz/9627c9ec-a36a-11e5-946c-0ea31932ec1d/viz.json')
//                .addTo(me.mapComponent.leafletMap)
//                .on('done', function(layer) {
//                  //do stuff
//                })
//                .on('error', function(err) {
//                  alert("some error occurred: " + err);
//                });
       }, 500);
	}

});