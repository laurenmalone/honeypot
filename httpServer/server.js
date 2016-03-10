/**
Copyright (c) MapBox
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
- Neither the name "MapBox" nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
**/

(function () {
    'use strict';
    console.info("                       _________                        __________   \\      /      __________    ____________   ____________");
    console.info("       /      /       /        /        /|       /     /              \\    /      /         /   /           /       /");
    console.info("      /      /       /        /        / |      /     /                \\  /      /         /   /           /       /");
    console.info("     /      /       /        /        /  |     /     /                  \\/      /         /   /           /       /");
    console.info("    /______/       /        /        /   |    /     /----------         /      /_________/   /           /       /");
    console.info("   /      /       /        /        /    |   /     /                   /      /             /           /       /");
    console.info("  /      /       /        /        /     |  /     /                   /      /             /           /       /");
    console.info(" /      /       /        /        /      | /     /                   /      /             /           /       /");
    console.info("/      /       /________/        /       |/     /___________        /      /             /___________/       /");
    
    console.log("Loading HoneyPot Server..........");
    console.log("Loading Express");
    var express = require('express');
    var app = express();
    console.log("Loading FS");
    var fs = require("fs");
    console.log("Loading SQLITE3: ");
    var dblite = require('sqlite3').verbose();
//	var dblite = require('/../../../../../usr/bin/sqlite3');
    var dbLocation = "HPTSERVER.db";
    console.log("Looking for DB at Location: " + dbLocation);
    var dbExists = fs.existsSync(dbLocation);
//    var resultObject = {"success": "", "rows": [], totalCount: 0};
    
    if(dbExists){
        app.get('/plugins', function (req, res) {
            console.log("Plugins Total Accessed");
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            var resultObject = {"success": true, "rows": [], totalCount: 0};
            var pluginObject = {"value":"", "display":"",  "count": 0};
            var pluginList = [];
            
            var finish = function() {
                db.close();
                res.jsonp({"rows": pluginList});
                console.log("close");
            };
            
            var addToObject = function (err, row) {
                pluginList.push({"value": row.value, "display": row.display})  
            };
            
            
            var getPlugins = function (err, row) {
                pluginList.push(row.value);
                this.row = row;
                var me = this;
                console.log("row", row.value);
                db.get("Select COUNT(*) from ?", row.value, function (err, row) {
                    console.log("row", row);
//                        pluginList.push({"count": row.count});
                });
            };
            
            db.serialize(function(){
                db.each("Select * from plugins", getPlugins);
                db.get("Select * from plugins", finish)
                
                
            });
            
            
            
        });
        
        app.get('/', function (req, res) {
            console.log("Plugins Accessed");
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            var resultObject = {"success": true, "rows": [], totalCount: 0};
            var selectCB = function (err, row) {
                console.log("Row", row);
                resultObject.rows = row;
                console.log("Result", resultObject);
                res.type('application/json');
                res.jsonp(resultObject);
                console.log("res");
                db.close();
                
            };
            
            var setTotalCount = function (err, row) {
                resultObject.totalCount = row.count;  
            };
            
            db.serialize(function(){
                
                db.get("Select COUNT(*) as count from plugins", setTotalCount);
                db.all("Select * from plugins", selectCB);

            });
        });
        
        app.get('/plugins/:id', function (req, res) {
            //get plugin table :id 
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            console.log("Plugin Table " + req.params.id + " Accessed");
            db.serialize(function(){

            });
            res.jsonp({value: req.params.id});
            db.close();
        });


        app.get('/plugins/:id/features', function (req, res) {
            //get plugin table :id Table Data
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            console.log("Sever Table " + req.params.id + "from IP " + req.ip);
            db.serialize(function(){

            });
            res.jsonp({value: req.params.id, feature: "GEOFEATURE"});
            db.close();
        });


        var server = app.listen(9005, function () {
        var host = server.address().address
        var port = server.address().port

        console.log("Honeypot HTTP SERVER Running on", port);

        });
    }else{
        console.log("DB was not found and the Server load was cancelled");
    }
}());

