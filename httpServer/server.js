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
    var dbLocation = "../honeypot.db";
    console.log("Looking for DB at Location: " + dbLocation);
    var dbExists = fs.existsSync(dbLocation);
    var db = new dblite.Database(dbLocation);

    if(dbExists){
        app.get('/plugins', function (req, res) {
            var db = new dblite.Database(dbLocation);
            var resultObject = {"success": true, "rows": [], totalCount: 0};
            var pluginObject = {"value":"", "display":"",  "count": 0};
            var pluginList = [];
            var count = 0;
            var tempObj = {};
            
            var finish = function() {   
                res.jsonp({"rows": pluginList, "count": pluginList.length });
                db.close();
            };
            db.serialize(function(){
                db.all("Select value from plugin", function(err, row){
                    //check to make sure database isn't empty
                    if(row && row.length > 0){
                        db.serialize(function(){
                            row.forEach(function (item){
                                db.serialize(function(){
                                    db.get("SELECT COUNT(*) as count from " + item.value, function(err, data){
                                        pluginList.push({ "count": data.count, "table": item.value});
                                    });   
                                });
                            });
                        });
                    }
                   
                  db.get("Select * from plugin", finish);  
                });   
            });
        });
        
        app.get('/', function (req, res) {
            var db = new dblite.Database(dbLocation);
            var resultObject = {"success": true, "rows": [], totalCount: 0};
             
            var selectCB = function (err, row) {
                if(!err){    
                    resultObject.rows = row;
                    res.type('application/json');
                    res.jsonp(resultObject);
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

                db.get("Select COUNT(*) as count from plugin", setTotalCount);
                db.all("Select * from plugin", selectCB);

            });

        });
        
        app.get('/plugins/:id', function (req, res) {
            //get plugin table :id 
            var db = new dblite.Database(dbLocation);
            var resultObject = {
                rows: [],
                totalCount: 0
            };
            var dbQueryCallback = function (err, row) {
                if(!err){
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
                db.all("Select * from " + req.params.id + " LIMIT " + req.query.limit + " OFFSET "+ (req.query.page * req.query.limit - req.query.limit) , dbQueryCallback);
            });    
        });

        app.get('/plugins/:table/features', function (req, res) {
            var dbFeatures = new dblite.Database(dbLocation);
            var pluginList = [];
            dbFeatures.all("Select * from " + req.params.table + " group by ip_address LIMIT 5000", function(err, ipList){
                //check to make sure database isn't empty
                if(ipList && ipList.length > 0){
                    pluginList = ipList; 
                }
                res.jsonp({"rows": pluginList });
                dbFeatures.close();   

            });   
              
        });

        app.get('/plugins/:table/weekdata', function (req, res) {
            var dbFeatures = new dblite.Database(dbLocation);
            var weekdata = [
                                {day: 'Sunday', data1: 0}, 
                                {day: 'Monday', data1: 0},
                                {day: 'Tuesday', data1: 0},
                                {day: 'Wednesday', data1: 0},
                                {day: 'Thursday', data1: 0},
                                {day: 'Friday', data1: 0},
                                {day: 'Saturday', data1: 0}
                            ];
            dbFeatures.all("Select * from " + req.params.table, function(err, data){
                //check to make sure database isn't empty
                
                if(data && data.length > 0){
                    data.forEach(function(item){
                        var timeS;
                        if(item.time_stamp){
                            timeS = new Date(item.time_stamp);
                            weekdata[timeS.getDay()].data1++; 
                        } else if(item.time){
                            timeS = new Date(item.time);
                            weekdata[timeS.getDay()].data1++; 
                        } else{
                            console.log('item.time_stamp and item.time do not exist. Check plugin definition.')
                        }
                        
                    });
                                  
                }
                res.jsonp({ "rows": weekdata });
                dbFeatures.close();   

            });   
              
        });

        var server = app.listen(444, function () {
        var host = server.address().address
        var port = server.address().port

        console.log("Honeypot HTTP SERVER Running on", port);

        });   

    } else {
        console.log("DB was not found and the Server load was cancelled");
    }
}());

