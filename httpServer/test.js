var supertest = require("supertest");
var should = require("should");
var should2 = require("should-http");

var server = supertest.agent("http://localhost:9005");

describe("Node Http Server Tests", function () {
	it ("Check to see if /index is invalid", function test(done) {
		server
		.get("/index")
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
    it ("Base Route should return an object", function test(done) {
        server
		.get("/")
		.expect("Content-type", /json/)
		.expect(200)
		.end(function(err,res){
			res.body.should.be.an.instanceOf(Object);
            done();
		});
	});
    it ("Base Route should return object with rows, totalCount properties", function test(done) {
        server
		.get("/")
		.expect("Content-type", /json/)
		.expect(200)
		.end(function(err,res){
            res.body.should.be.an.instanceOf(Object).and.have.properties(['rows', "totalCount"]);
            done();
		});
	});
    it ("plugins/:id route should be available", function test(done) {
		server
		.get("/plugins/telnet")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
			done();
		});
	});
    it ("plugins/:id route should return an object with property rows, totalCount", function test(done) {
		server
		.get("/plugins/telnet")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
          res.body.should.have.properties(['rows', 'totalCount']);
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
    it ("plugins/:id/features route should return an object with properties rows and totalCount", function test(done) {
		server
		.get("/plugins/id/features")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
          res.body.should.have.properties(['rows', 'totalCount']);
			done();
		});
	});
    it ("plugins/:id/features route should return a json", function test(done) {
		server
		.get("/plugins/id/features")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
            res.should.be.json();
			done();
		});
	});
	id("plugins/:table/weekdata route should return a json", function test(done){
		server
		.get("/plugins/:table/weekdata")
		.expect("Content-type",/json/)
		.expect(200)
		.end(function(err,res){
			res.should.be.json();
			done();
		});
	});

});
