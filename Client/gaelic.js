var qnumber = 1;
var score = 0;
var answered = 0;

/*globals $, popupConfirm, popupAlert, userEmail URL */
var URL = "http://localhost:8080/";

$(document).ready(function(){
    $( "#loginForm" ).submit(function( event ) {
        doLogin();
    });
    $("#addPurchase").click(function(){
        getPurchaseData();

    });
    $("#translateWord").on('click', doTranslate);
    $("#grammar").on('click',doGet);
    $("#next").on('click', upQuestion);
    $("#previous").on('click', upQuestion);
    $("#login").on('click', goLogin);
    $("#cancel").on('click', goHome);
});

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

function answerBox() {
    answered++;
    if ($(this).text() == answer){
        alert("Correct!");
        score++
    }
    else
        alert("Eh...er, the answer was " + answer);

    upQuestion();
    if(answered==3){
        alert("You scored " + score);
        answered=0;
        score=0;
    }

}

function upQuestion(){
    qnumber++;
    if(qnumber>2)
        qnumber=0;

    doGet();
}

function downQuestion(){
    qnumber--;
    if(qnumber<0)
        qnumber=2;

    doGet();
}

function doTranslate() {
    $.ajax({
        type: "GET",
        url: URL + "translateWord/" + $("#singleWord").val(),
        async: true,
        contentType: "application/javascript",
        dataType: 'jsonp',
        success: function (json) {
            handleWord(json);
        },
        error: function (e) {
            popupConfirm("Error", e.message);
            alert("failure");
        }
    });
}

function doGet() {
    $.ajax({
        type: "GET",
        url: URL + "users/neil@bedrock.com",
        async: true,
        contentType: "application/javascript",
        dataType: 'jsonp',
        success: function (json) {
            handleJsonResponse(json);

        },
        error: function (e) {
            popupConfirm("Error", e.message);
            alert("failure");
        }
    });
}

function handleJsonResponse(json) {
    var index, html = "";
    //for(index=json.length-1; index>=0; index--){
    html += formatMessage(json[qnumber]);
    //}
    answer=json[qnumber].answer;
    $("#questions").html(html).listview('refresh');
    $("#opt1").on('click', answerBox);
    $("#opt2").on('click', answerBox);
    $("#opt3").on('click', answerBox);
    $("#opt4").on('click', answerBox);
}

function handleWord(json) {
    var index, html = "";
    for(index=json.length-1; index>=0; index--){
        $("#answer").val((json[0].gaelicWord));
    }
}

function formatMessage(ques) {
    html = "<li><div class='ui-li-desc'>" + "<h5 style ='white-space:normal;' class='ui-li-heading'>" + ques.message + "</h5>" +
        "<li>" + "<a class ='choose' id='opt1' href='#'>" + ques.opt1 + "</a>" + "</li>" +
        "<li>" + "<a class ='choose' id='opt2' href='#'>" + ques.opt2 + "</a>" + "</li>" +
        "<li>" + "<a class ='choose' id='opt3' href='#'>" + ques.opt3 + "</a>" + "</li>" +
        "<li>" + "<a class ='choose' id='opt4' href='#'>" + ques.opt4 + "</a>" + "</li>";
    html += "</div></li>";
    return html;

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