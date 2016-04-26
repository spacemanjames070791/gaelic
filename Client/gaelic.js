var qnumber = 1;
var score = 0;
var answered = 0;

/*globals $, popupConfirm, popupAlert, userEmail URL */
//var URL = "http://gaelic-1281.appspot.com/";
var URL = "http://localhost:8080/";
localStorage.setItem("loggedin", 1);
localStorage.setItem("currentuser", "Neil");

$(document).ready(function(){

    if(localStorage.loggedin==1)
        $("#signin").text("Logout");
    if(!!navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(handlePosition);
        }
    $("#translateWord").on('click', doTranslate);
    $("#quiz").on('click',doGet);
    $("#next").on('click', upQuestion);
    $("#previous").on('click', upQuestion);
    $("#login").on('click', goLogin);
    $("#cancel").on('click', goHome);
});

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
    //if(localStorage.loggedin==1) {
        $.mobile.changePage("#quizpage");
        $("#currentUser").text(localStorage.currentuser);
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
    //}
    //else
        //alert("You need to login to use the quiz section");
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