window.onload = function(){
    displayMessage();
};

function displayMessage(){
    var mess = document.getElementById('notify');
    mess.style.display = "block";

    setTimeout( function() {
        mess.style.display = "none";
    }, 5000
    );
}