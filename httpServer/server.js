(function () {
    'use strict';

    var express = require('express');
    var app = express();
    var fs = require("fs");

    app.get('/plugins', function (req, res) {
        console.log("Sever Accessed")
        //get plugin Data
        var result = JSON.stringify({
                "success": true,
                "rows": [{
                    "value": "all",
                    "display": "All",
                    "orm": '{"fields":[{"name":"Plugin","type":"string"},{"name":"Hits","type":"integer"}]}'
                }, {
                    "value": "telnet",
                    "display": "Telnet",
                    "orm": '{"fields":[{"name":"area_code","type":"integer"},{"name":"city","type":"string"}]}'
                }],
                totalCount: 2
            }, 0, 4);
        res.end(result);
    });
    
    app.get('/plugins/:id', function (req, res) {
        //get plugin :id Table Data
        console.log("Sever Accessed id", req.params.id);
    });
    


    var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port

    console.log("Honeypot HTTP SERVER Running on", port);
    console.log("                       _________                        __________   \\      /      __________    ____________   ____________");
    console.log("       /      /       /        /        /|       /     /              \\    /      /         /   /           /       /");
    console.log("      /      /       /        /        / |      /     /                \\  /      /         /   /           /       /");
    console.log("     /      /       /        /        /  |     /     /                  \\/      /         /   /           /       /");
    console.log("    /______/       /        /        /   |    /     /----------         /      /_________/   /           /       /");
    console.log("   /      /       /        /        /    |   /     /                   /      /             /           /       /");
    console.log("  /      /       /        /        /     |  /     /                   /      /             /           /       /");
    console.log(" /      /       /        /        /      | /     /                   /      /             /           /       /");
    console.log("/      /       /________/        /       |/     /___________        /      /             /___________/       /");
    });
}());

