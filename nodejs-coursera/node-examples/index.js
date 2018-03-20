var rect = require("./rectangle");

function solveRect(l, b) {
    console.log("Solving for rectangle with l = " + l + " and b = " + b);
    
    rect(l, b, (err, rec) => {
        if (err) {
            console.log("ERROR:", err.message);
        }
        else {
            console.log("Area:", rec.area());
            console.log("Perimeter:", rec.perimeter)
        }
    });
    console.log("this statement is after the call to rect!")
}

solveRect(2,4);
solveRect(3,5);
solveRect(0,5);
solveRect(2,-9)