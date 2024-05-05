function runFunctions() {
    function1().then(function(checkerResult) {
        if (checkerResult) {
            function2();
        } else {
            console.log("Email verification failed");
        }
    }).catch(function(error){
        alert(error);
    });
}

function function1() {
    return new Promise(function(resolve, reject){
        var email = document.getElementById("reciever_email").value;
        var pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (pattern.test(email)) {
            resolve(true); 
        } else {
            reject("Invalid email"); 
        }
    });    
}

function function2() {
    //first part 
    var div = document.getElementById("box1");
    div.style.display = "block";
}


