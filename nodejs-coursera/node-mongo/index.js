const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const dboper = require("./operations");

const url = 'mongodb://127.0.0.1:27017/confusion';

MongoClient.connect(url, (err, client) => {
    assert.equal(err, null);
    console.log('Connected successfully to server');

    const db = client.db("confusion");

    // insert first doc
    dboper.insertDocument(db, 
        { name: "FlowerPizza", description: "first pizza" }, 
        "dishes", (res) => {
            console.log("Insert Document:\n", res.ops);

            // find all docs
            dboper.findDocument(db, "dishes", (docs) => {
                console.log("Found documents:\n", docs);

                // update the only doc
                dboper.updateDocument(db, 
                    {name: "FlowerPizza"}, // specify the document by name
                    {description: "updated pizza"}, // update value
                    "dishes", (res) => {
                        console.log("Updated document:\n", res.result);

                        // check the updated doc
                        dboper.findDocument(db, "dishes", (docs) => {
                            console.log("Found updated documents:\n", docs);

                            // remove collection
                            db.dropCollection("dishes", (err, result) => {
                                assert.equal(err, null);
                                client.close();
                            });
                        });
                    });
            });
        });

    /* traditional way
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
    */
    
});