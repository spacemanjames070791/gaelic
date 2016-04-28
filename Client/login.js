/**
 * Created by Neil on 25/04/2016.
 */

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
        type: "POST",
        url: URL + "register",
        data: {email:$("#registeremail").val(), password:$("#registerpassword").val(), username:$("#firstname").val()}
    }).done(function (data, textStatus, jqXHR) {
        // The AJAX call was successful, so we can clear out the message field.
        console.log("OK");
    }).fail(function (data, errStatus) {
        console.log("Crap happened!");
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

function goHome() {
    $.mobile.changePage("#home");
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

function goLogin(){
    alert("Login");
    var user = $("#useremail").val(), pwd = $("#userpassword").val();
    localStorage.setItem("user", {user: user, password: pwd});
    goHome();
}
