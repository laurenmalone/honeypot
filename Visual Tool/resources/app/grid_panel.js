Ext.define("grid_panel",{
    extend: 'Ext.grid.Panel',
    itemId: 'table_grid_panel',
    region: "center",
    title: 'Table',
    border: false,
    initComponent: function (){
		this.columns = [];
		Ext.apply(this, {
			columns: this.columns
			});
		this.callParent();
	},
    /**
    This method uses the orm object to set the columns of the table. The plugin param is the store to attach to the table.
    @param {string} plugin - The name of the store to load. 
    @param {object} orm - Object that describes the data that will be displayed
    **/
    setStoreColumns: function (orm, plugin) {
        var me = this;
        this.columns = [];
        orm.forEach(function(item){
            if(item.name !== 'feature'){
                me.columns.push({text: item.name, dataIndex: item.name, flex: 1});
            }
        });
        var theStore = (Ext.StoreMgr.lookup(plugin)) ? Ext.StoreMgr.lookup(plugin) : this.createNewStore(orm, plugin);
        this.reconfigure(theStore, this.columns);
    },
      /**
    This method creates a data store and autoloads that data.
    @param {string} plugin - The name of the store to load. 
    @param {object} orm - Object that describes the data that will be displayed
    **/  
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
    },
    
    dockedItems: [{
        xtype: 'pagingtoolbar',
        store: null,
        dock: 'bottom'
    }]


});