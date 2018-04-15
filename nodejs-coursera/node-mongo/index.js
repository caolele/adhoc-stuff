const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const url = 'mongodb://127.0.0.1:27017/confusion';
MongoClient.connect(url, (err, client) => {
    assert.equal(err, null);
    console.log('Connected successfully to server');
    const db = client.db("confusion");
    const collection = db.collection('dishes');
    collection.insertOne({"name": "FlowerPizza", "description": "yet another pizza"}, (err, result) => {
        assert.equal(err, null);
        console.log('After Insert:\n');
        console.log(result.ops);
        collection.find({}).toArray((err, docs) => {
            assert.equal(err, null);
            console.log("Found:\n");
            console.log(docs);
            db.dropCollection("dishes", (err, result) => {
                assert.equal(err, null);
                client.close();
            });
        });
    });
});