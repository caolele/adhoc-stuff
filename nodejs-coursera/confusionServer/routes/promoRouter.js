const express = require("express");
const bodyParser = require("body-parser");

const promotionRouter = express.Router();
promotionRouter.use(bodyParser.json());

//http://localhost:3000/promotions
promotionRouter.route("/")
.all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader("Content-Type", "text/plain");
    next();
})
.get((req, res, next) => {
    res.end("Will send all the promotions to you.");
})
.post((req, res, next) => {
    res.end("Will create a promotion for you: " + req.body.name 
            + ", with details: " + req.body.description);
})
.put((req, res, next) => {
    res.statusCode = 403;
    res.end("PUT not supported on /promotions");
})
.delete((req, res, next) => {
    res.end("Deleting all the promotions!!!");
});

//http://localhost:3000/promotions/:promotionId
promotionRouter.route("/:promotionId")
.all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader("Content-Type", "text/plain");
    next();
})
.get((req, res, next) => {
    res.end("Will send to you the promotion: " + req.params.promotionId);
})
.post((req, res, next) => {
    res.statusCode = 403;
    res.end("POST operation not supported on /promotions/" + req.params.promotionId);
})
.put((req, res, next) => {
    res.write("Will update promotion: " + req.params.promotionId + "\n");
    res.end("promotion name: " + req.body.name + ", details: " + req.body.description);
})
.delete((req, res, next) => {
    res.end("Deleting promotion: " + req.params.promotionId);
});

module.exports = promotionRouter;