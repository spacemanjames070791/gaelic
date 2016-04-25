/**
 * Created by Neil on 25/04/2016.
 */
var URL = "http://gaelic-1281.appspot.com/";
//var URL = "http://localhost:8080/";

$(document).ready(function(){
    $( "#loginForm" ).submit(function( event ) {
        doLoginProcess();
    });
    $("#login").on('click', goLogin);
    $("#cancel").on('click', goHome);
});

function doLoginProcess() {
    $.ajax({
        type: "GET",
        url: URL + "login/" + $("#useremail").val() + "/" + $("#userpassword").val(),
        async: true,
        contentType: "application/javascript",
        dataType: 'jsonp',
        success: function (json) {
            checkCredentials(json);

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

function checkCredentials(json){
    for(index=0;index<json.length; index++){
    }
    if ($("#userpassword").val()==json[0].password){
        alert("Login successful");
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
