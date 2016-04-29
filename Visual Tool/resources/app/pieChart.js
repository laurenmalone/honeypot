Ext.define('center_piechart', {
    extend: 'Ext.Panel',
    region: "center",
    width: 650,
    initComponent: function() {
        var me = this;
        me.items = [{
            xtype: 'polar',
            width: '100%',
            itemId: "pieChart",
            height: '100%',
            store: {},
            insetPadding: 30,
            innerPadding: 20,
            legend: {
                docked: 'bottom'
            },
            interactions: ['rotate', 'itemhighlight'],
            sprites: [{
                type: 'text',
                text: 'Plugin Hits',
                fontSize: 22,
                width: 100,
                height: 30,
                x: 40, 
                y: 20  
            }, {
                type: 'text',
                text: 'Data: CS4260 Honeypot',
                x: 12,
                y: 425
            }, {
                type: 'text',
                text: 'Source: 73.78.7.177',
                x: 12,
                y: 440
            }],
            series: [{
                type: 'pie',
                animation: {easing: 'easeOut', duration: 500},
                angleField: 'data1',  
                clockwise: false,
                highlight: {
                    margin: 20
                },
                label: {
                    field: 'name',       
                    display: 'outside',
                    font: '14px Arial'
                },
                style: {
                    strokeStyle: 'white',
                    lineWidth: 1
                },
                tooltip: {
                    trackMouse: true,
                    renderer: function(tooltip, storeItem, item) {
                        tooltip.setHtml(storeItem.get('name') + ': ' + storeItem.get('data1') + '%');
                    }
                }
            }]
        }];
        this.callParent();
    }
});