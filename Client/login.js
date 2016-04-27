/**
 * Created by Neil on 25/04/2016.
 */
var URL = "http://gaelic-1281.appspot.com/";
//var URL = "http://localhost:8080/";

$(document).ready(function(){
    $( "#registerForm" ).submit(function( event ) {
        doRegister();
    });
    $("#login").on('click', goLogin);
    $("#cancel").on('click', goHome);
    $("#ok").on('click', doLoginProcess);
});

function doRegister(){
    $.ajax({
        type: "GET",
        url: URL + "register?email=" + $("#registeremail").val() + "&username=" + $("#firstname").val() + "&password="
        + $("#registerpassword").val(),
        async: true,
        contentType: "application/javascript",
        dataType: 'jsonp',
        success: function (json) {
            alert("added user");
        },
        error: function (e) {
            popupConfirm("Error", e.message);
            alert("failure");
        }
    });
}

function doLoginProcess() {
    $.ajax({
        type: "GET",
        url: URL + "login/" + $("#useremail").val() + "/" + $("#userpassword").val(),
        async: true,
        contentType: "application/javascript",
        dataType: 'jsonp',
        success: function (json) {
            if($("#useremail").val()=="")
                alert("Please enter your username");
            else if($("#userpassword").val()=="")
                alert("Please enter you password");
            else if(json=="")
                alert("Email address not found");
            else
                checkCredential(json);

        },
        error: function (e) {
            popupConfirm("Error", e.message);
            alert("failure");
        }
    });
}

function goLogin(){
    alert("Login");
    var user = $("#useremail").val(), pwd = $("#userpassword").val();
    localStorage.setItem("user", {user: user, password: pwd});
    goHome();
}

function goHome() {
    $.mobile.changePage("#home");
}

function checkLogin() {
    return localStorage.login != null;
}

function checkCredential(json){
    for(index=0;index<json.length-1; index++){
    }
    if ($("#userpassword").val()==json[0].password){
        alert("Login successful");
        localStorage.setItem("loggedin", 1);
        localStorage.setItem("currentuser", json[0].username);
        $.mobile.changePage("#home");
    }else{
        alert("Login failed");
    }
}

function doLogin() {
    alert("notLoggedIn");
    var notLoggedIn = true;
    if(!checkLogin()) {
        popupLogin(function okFunc(){
            var result = getLoginValues();
            localStorage.setItem("login", result);
            notLoggedIn = false;
        }, function cancelFunc(){
            notLoggedIn = true;
        });
    }

    if(notLoggedIn) {
        popupAlert("You need to be logged in!");
    }
}