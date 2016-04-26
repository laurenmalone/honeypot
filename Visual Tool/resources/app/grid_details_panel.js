Ext.define("grid_details_panel",{
	extend: 'Ext.panel.Panel',
	itemId: 'grid_details_panel',
	layout: 'border',
	initComponent: function (){
		this.grid_panel = Ext.create("grid_panel");
		
		this.grid_html_panel = Ext.create("Ext.panel.Panel",{
				region: "south",
				itemId: "detailsPanel",
				collapsible: true,
				title: "Details",
				height: "35%",
				split: true,
				html: '<p>Please Select A Table Value</p>'
			});
		var me = this;
		this.grid_panel.on('rowclick', function(context, record, tr, index, e) {
			console.log("app_controller row click", record, tr, index);
			var html = "<div class='container' style='width: 100%;padding-bottom: 12px; padding-left: 30px;'>";
			this.details = '';
			this.pluginnName = '';
			var context = this;
			html += "<div class='jumbotron'>"
			Ext.getStore('plugins').each(function (item) {
				if(item.data.value !== 'all'){
					if(item.data.value === record.data.table || item.data.value === record.store.storeId){
						context.pluginName = item.data.display;
						context.details = item.data.description; 
					}
				}
			});
			html += "<h2>" + this.pluginName + "</h2>";
			html += "<p>" + this.details + "</p>";
			html += "</div>"
			for(var prop in record.data){
				if(prop !== "id" && prop !== "feature"){
					console.log(prop, record.data[prop]);
					html += "<p>" + prop + ": " + record.data[prop] + "</p>";
				}
			}
			html += "</div> "
			me.grid_html_panel.update(html);
		});
		
		Ext.apply(this, {
			items:[this.grid_panel, this.grid_html_panel]
			});
		this.callParent();
	}
});