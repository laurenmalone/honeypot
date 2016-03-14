var supertest = require("supertest");
var should = require("should");

var server = supertest.agent("http://localhost:9005");

describe("Http Server Tests", function () {
	// #1 should return list of plugins
	it ("should fail!!", function test(done) {
		server
		.get("/")
	//	.expect("Content-type",/json/)
		.expect(404)
		.end(function(err,res){
			res.status.should.equal(404);
			done();
		});
	});



});
