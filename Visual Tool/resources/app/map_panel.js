Ext.define('map_panel', {
	extend: 'CartoDBPanel',
	itemId: 'map_panel',
	border: false,
	initComponent: function () {
		this.baselayer = {
			positron: {
				url: 'http://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png',
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
			}
		};
		this.callParent();
	},

	changeBaseMap: function (layer) {
		this.mapComponent.setBaseLayer(this.baselayer[layer]);
	},

	afterRender: function () {
		var me = this;
		setTimeout(function () {
			me.mapComponent.setBaseLayer(me.baselayer.positron);
       }, 500);
	}

});