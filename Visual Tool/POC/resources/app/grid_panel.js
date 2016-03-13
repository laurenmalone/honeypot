Ext.define("grid_panel",{
    extend: 'Ext.grid.Panel',
    itemId: 'table_grid_panel',
    title: 'grid',
    border: false,
//    columns: [
//        {text: 'IP Address', dataIndex: 'ipAddress', flex: 3},
//        {text: 'Login Value', dataIndex: 'loginValue', flex: 1},
//        {text: 'Password', dataIndex: 'password', flex: 1},
//        {text: 'Family', dataIndex: 'family', flex: 1},
//        {text: 'Type', dataIndex: 'type', flex: 3},
//        {text: 'Proto', dataIndex: 'proto', flex: 1}
              
//    ],
    
    initComponent: function (){
		
        this.columns = [];
		Ext.apply(this, {
			columns: this.columns
			});
		this.callParent();
	},
    
    setStoreColumns: function (orm, plugin) {
        var me = this;
        this.columns = [];
        orm.forEach(function(item){
             me.columns.push({text: item.name, dataIndex: item.name, flex: 1})
        });
//        this.getTheresetGrid();
//        this.removeGridData();
        
        var theStore = (Ext.StoreMgr.lookup(plugin)) ? Ext.StoreMgr.lookup(plugin) : this.createNewStore(orm, plugin);
        this.reconfigure(theStore, this.columns);
    },
    
    createNewStore: function(orm, plugin) {
        var urlPath = './resources/app/jsons/' + plugin + "/tableData.json"
        var newStore = Ext.create('Ext.data.Store', {
            storeId: plugin + "data",
            fields: orm,
            proxy: {
                type: 'jsonp',
                url: urlPath,
                reader: {
                    type: 'json',
                    rootProperty: 'rows'
                }
            },
            autoLoad: true
        });
        return newStore;
    }


});