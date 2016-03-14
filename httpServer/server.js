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
    
    
    var db = new dblite.Database(dbLocation);
//    PRAGMA table_info(plugins)
    // SELECT name as value FROM sqlite_master WHERE type = "table"
    if(dbExists){
        app.get('/plugins', function (req, res) {
            console.log("Plugins Total Accessed");
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            var resultObject = {"success": true, "rows": [], totalCount: 0};
            var pluginObject = {"value":"", "display":"",  "count": 0};
            var pluginList = [];
            var count = 0;
            var tempObj = {};
            
            var finish = function() {
                db.close();
                console.log("response sent");
                res.jsonp({"rows": pluginList, "count": pluginList.length });
                console.log("close");
            };
            
//             var addToObject = function (err, data) {
//                 console.log("add to object");
//                 pluginList.push({"count": data, "table": tempObj.value});
                
//             };
            
            
//             var getPlugins = function (err, row) {
//                 console.log("get row", row);
//                 row.forEach(function (item){
//                     tempObj = item;
//                     console.log(" this is temp obj" + tempObj);
//                     db.all("SELECT COUNT(*) from " + item.value, addToObject )
//                     //pluginList.push(item);
// //                    db.
// //                    pluginList.push({value: item.value, count:    
//                 });
//             };
            
            db.serialize(function(){
                db.all("Select value from plugins", function(err, row){
                   console.log("get row", row);
                   db.serialize(function(){
                    row.forEach(function (item){
                        tempObj = item;
                        console.log(" this is temp obj" + tempObj);
                        db.serialize(function(){
                            db.get("SELECT COUNT(*) as count from " + item.value, function(err, data){
                                console.log("add to object " + tempObj.value);
                                pluginList.push({ "count": data.count, "table": tempObj.value});
                            }); 
                            db.get("", finish);   
                        });
                    });
                });
                });
                
            });
        });
        
        app.get('/', function (req, res) {
            console.log("Plugins Accessed");
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            var resultObject = {"success": true, "rows": [], totalCount: 0};
            
            
            var selectCB = function (err, row) {
                if(!err){    
                    console.log("Row", row);
                    resultObject.rows = row;
                    console.log("Result", resultObject);
                    res.type('application/json');
                    res.jsonp(resultObject);
                    console.log("res");
                    db.close();
                }else{
                    console.log("Error: ", err);
                    res.sendStatus(406);
                    db.close();
                }
            };
            
            var setTotalCount = function (err, row) {
                if(!err){
                    resultObject.totalCount = row.count;  
                }else{
                    console.log("Error: ", err);
                }
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
            var resultObject = {
                    rows: [],
    
                totalCount: 0
            };
            var dbQueryCallback = function (err, row) {
                if(!err){
                    console.log("plugins/:id row", row, err);
                    resultObject.rows = row;
                    res.jsonp(resultObject);
                    db.close(); 
                }else{
                    console.log('err', err);
                    res.sendStatus(406);
                    db.close(); 
                }
            };
            

            var setTotalCount = function (err, row) {
                if(!err){
                    resultObject.totalCount = row.count;  
                }else{
                    resultObject.error = err;
                    console.log('err', err);
                }


            };

            db.serialize(function(){
                db.get("Select COUNT(*) as count from " + req.params.id, setTotalCount);
                db.all("Select * from " + req.params.id, dbQueryCallback);
            });
            
            
        });


        app.get('/plugins/:id/features', function (req, res) {
            //get plugin table :id Table Data
            console.log("Opening DB at location: " + dbLocation);
            var db = new dblite.Database(dbLocation);
            console.log("Sever Table " + req.params.id + "from IP " + req.ip);
            
            var returnFeature = function (err, row) {
                res.jsonp({value: row, totalCount: -1});
                db.close();
            };
            
            db.serialize(function(){
                db.all("Select feature from " + req.params.id, returnFeature);     
            });    
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

