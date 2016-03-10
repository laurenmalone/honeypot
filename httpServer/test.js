var supertest = require("supertest");
var should = require("should");


var server = supertest.agent("http://localhost:9005");

describe("Http Server Tests", function () {
	// #1 should return list of plugins
	it ("Check to see if /index is invalid", function test(done) {
		server
		.get("/index")
	//	.expect("Content-type",/json/)
		.expect(404)
		.end(function(err,res){
			res.status.should.equal(404);
			done();
		});
	});
    it ("Base route should be available", function test(done) {
		server
		.get("/")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
			res.status.should.equal(200);
			done();
		});
	});
//    it ("Base Route should return plugins list", function test(done) {
//        server
//		.get("/")
//		.expect("Content-type",/json/)
//		.expect(200)
//		.end(function(err,res){
//			res.status.should.equal(200);
//            should.deepEqual(res.body, {"success":true,"rows":
//                                        [{"value":"all",
//                                          "orm":"{\"fields\":[{\"name\":\"Plugin\",\"type\":\"string\"},{\"name\":\"Hits\",\"type\":\"integer\"}]}",
//                                          "display":"All"},
//                                         {"value":"telnet",
//                                          "orm":"{\"fields\":[{\"name\":\"area_code\",\"type\":\"integer\"},{\"name\":\"city\",\"type\":\"string\"}]}",
//                                          "display":"Telnet"}],"totalCount":2});
//            done();
//		});
//	});
    it ("Base Route should return object with rows properties", function test(done) {
        server
		.get("/")
		.expect("Content-type", /json/)
		.expect(200)
		.end(function(err,res){
			res.body.should.have.property('rows');
            done();
		});
	});
    it ("plugins/:id route should be available", function test(done) {
		server
		.get("/plugins/id")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
			res.status.should.equal(200);
			done();
		});
	});
    it ("plugins/:id route should return an object with property name", function test(done) {
		server
		.get("/plugins/id")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
          res.body.should.have.properties(['value']);
			done();
		});
	});
    it ("plugins/:id/features route should be available", function test(done) {
		server
		.get("/plugins/id/features")
		.expect("Content-type", /json/)
		.expect(200)
		.end(function(err,res){
			res.status.should.equal(200);
			done();
		});
	});
    it ("plugins/:id/features route should return an object with properties value and feature", function test(done) {
		server
		.get("/plugins/id/features")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
          res.body.should.have.properties(['value', 'feature']);
			done();
		});
	});

});
