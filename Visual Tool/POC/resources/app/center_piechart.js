Ext.define("center_piechart",{
    extend: "Ext.chart.PolarChart",
    region: "center",
    insetPadding: 50,
    innerPadding: 20,
//    width: 500,
//    height: 500,
    store: Ext.create('Ext.data.JsonStore', {
            fields: ['os', 'data1' ],
            data: [
                { os: 'Android', data1: 68.3 },
                { os: 'BlackBerry', data1: 1.7 },
                { os: 'iOS', data1: 17.9 },
                { os: 'Windows Phone', data1: 10.2 },
                { os: 'Others', data1: 1.9 }
            ]
        }),
    legend: {
        docked: 'bottom'
    },
    interactions: ['rotate', 'itemhighlight'],
//    sprites: [{
//        type: 'text',
//        text: 'Pie Charts - Basic',
//        font: '22px Helvetica',
//        width: 100,
//        height: 30,
//        x: 40, // the sprite x position
//        y: 20  // the sprite y position
//    }, {
//        type: 'text',
//        text: 'Data: IDC Predictions - 2017',
//        font: '10px Helvetica',
//        x: 12,
//        y: 425
//    }, {
//        type: 'text',
//        text: 'Source: Internet',
//        font: '10px Helvetica',
//        x: 12,
//        y: 435
//    }],
    series: [{
        type: 'pie',
        angleField: 'data1',
        label: {
            field: 'os',
            display: 'outside',
            calloutLine: {
                length: 60,
                width: 3
                // specifying 'color' is also possible here
            }
        },
        highlight: true,
        tooltip: {
            trackMouse: true,
            renderer: function(storeItem, item) {
                this.setHtml(storeItem.get('os') + ': ' + storeItem.get('data1') + '%');
            }
        }
    }]
});