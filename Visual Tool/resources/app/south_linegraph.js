Ext.define("south_linegraph",{
    extend: "Ext.chart.CartesianChart",
    itemId: "lineGraph",
    insetPadding: 40,
    innerPadding: {
        left: 40,
        right: 40
    },
    sprites: [{
        type: 'text',
        text: 'Attacks by Day of Week',
        font: '22px Helvetica',
        width: 100,
        height: 30,
        x: 40, // the sprite x position
        y: 20  // the sprite y position
    }, {
        type: 'text',
        text: 'Data: Browser Stats 2012',
        font: '10px Helvetica',
        x: 12,
        y: 470
    }, {
        type: 'text',
        text: 'Source: http://www.w3schools.com/',
        font: '10px Helvetica',
        x: 12,
        y: 480
    }],
    axes: [{
        type: 'numeric',
        fields: 'data1',
        position: 'left',
        grid: true,
        minimum: 0,
        maximum: 10000,
//        renderer: function (v) { 
//            console.log("V", v);
//            return v.name + '%'; 
//        }
    }, {
        type: 'category',
        fields: 'day',
        position: 'bottom',
        grid: true,
        label: {
            rotate: {
                degrees: -45
            }
        }
    }],
    series: [{
        type: 'line',
        xField: 'day',
        yField: 'data1',
        style: {
            lineWidth: 4
        },
        marker: {
            radius: 4
        },
        label: {
            field: 'data1',
            display: 'over'
        },
        highlight: {
            fillStyle: '#000',
            radius: 5,
            lineWidth: 2,
            strokeStyle: '#fff'
        },
        tooltip: {
            trackMouse: true,
            style: 'background: #000',
            showDelay: 0,
            dismissDelay: 0,
            hideDelay: 0,
            renderer: function(tooltip, storeItem, item) {
                tooltip.setHtml(storeItem.get('day') + ': ' + storeItem.get('data1'));
            }
        }
    }]

});