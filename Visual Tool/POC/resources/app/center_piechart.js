Ext.define("center_piechart",{
    extend: "Ext.chart.PolarChart",
    itemId: "pieChart",
    region: "center",
    animation: false,
    insetPadding: 50,
    innerPadding: 20,
    style: {
        width: "100%",
        height: "100%"
    },
    legend: {
        docked: 'bottom'
    },
    interactions: ['rotate', 'itemhighlight'],
    sprites: [{
        type: 'text',
        text: 'All plugins as percent of total',
        font: '22px Helvetica',
        width: 100,
        height: 30,
        x: 40, 
        y: 20  
    }, {
        type: 'text',
        text: 'CS4260 HoneyPot',
        font: '10px Helvetica',
        x: 12,
        y: 425
    }, {
        type: 'text',
        text: 'Source: 73.78.8.177',
        font: '10px Helvetica',
        x: 12,
        y: 435
    }],
    series: [{
        type: 'pie',
        angleField: 'data1',
        label: {
            field: 'name',
            display: 'outside',
            calloutLine: {
                length: 60,
                width: 3
            }
        },
        highlight: true,
        tooltip: {
            trackMouse: true,
            renderer: function(tooltip, storeItem, item) {
                tooltip.setHtml(storeItem.get('name') + ': ' + storeItem.get('data1') + '%');
            }
        }
    }]
});