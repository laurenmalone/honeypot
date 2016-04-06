Ext.define('CartoDBPanel', {
	extend: 'Ext.panel.Panel',
	alias: 'cartodbpanel',
	layout: 'fit',
	initComponent: function () {
		this.mapComponent = Ext.create('CartoDBComponent', {
		});
        
		this.items = [this.mapComponent];
		this.callParent(arguments);
		
	}
});