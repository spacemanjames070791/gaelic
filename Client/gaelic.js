var qnumber = 0;
var score = 0;
var answered = 0;
var totalQuestions = 0;

/*globals $, popupConfirm, popupAlert, userEmail URL */
//var URL = "http://gaelic-1281.appspot.com/";
var URL = "http://localhost:8080/";
localStorage.setItem("loggedin", 1);
localStorage.setItem("currentuser", "Neil");

$(document).ready(function(){
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
        score++;
    }

    upQuestion();
    if(answered==totalQuestions){
        alert("You scored " + score);
        answered=0;
        score=0;
        $.mobile.changePage("#home");
    }

}

function upQuestion(){
    qnumber++;
    if(qnumber>totalQuestions)
        qnumber=0;

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
    if(localStorage.getItem("loggedin")==1){
        $("#currentUser").text(localStorage.currentuser);
        $.ajax({
            type: "GET",
            url: URL + "questions",
            async: true,
            contentType: "application/javascript",
            dataType: 'jsonp',
            success: function (json) {
                totalQuestions = json.length;
                handleJsonResponse(json);
            },
            error: function (e) {
                popupConfirm("Error", e.message);
                alert("failure");
            }
        });
    }
    else {
        $("#questions").html('<p>You need to log in to access the quiz section</p>' +
        '<a id="signin" data-role="button" href="#loginPage">Sign In</a>')
    }
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

