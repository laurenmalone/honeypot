Ext.define("grid_panel",{
    extend: 'Ext.grid.Panel',
    itemId: 'table_grid_panel',
    title: '',
    border: false,
    columns: [
        {text: 'IP Address', dataIndex: 'ipAddress', flex: 3},
        {text: 'Login Value', dataIndex: 'loginValue', flex: 1},
        {text: 'Password', dataIndex: 'password', flex: 1},
        {text: 'Family', dataIndex: 'family', flex: 1},
        {text: 'Type', dataIndex: 'type', flex: 3},
        {text: 'Proto', dataIndex: 'proto', flex: 1}
              
    ],
    initComponent: function (){
		

		Ext.apply(this, {
			
			});
		this.callParent();
	}


});