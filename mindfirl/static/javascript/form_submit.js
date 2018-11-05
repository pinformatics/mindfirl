/*
    Author: Qinbo Li
    Date: 12/22/2017
    Requirement: jquery-3.2.1, clickable.js
    This file is for form submit, and sending user click data
*/

function post(path, params, method) {
    // COPYRIGHT: https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit
    method = method || "post"; // Set method to post by default if not specified.
    var formData = new FormData();
    formData.append("user_data", params);
    var request = new XMLHttpRequest();
    request.open("POST", path);
    request.send(formData);
}

function get_summitted_answers() {
    var c = $(".ion-android-radio-button-on").each(function() {
        $type = "type:final_answer";
        $this_click = "value:" + this.id;
        var dt = new Date();
        $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
        $url = "url:" + $THIS_URL;
        $data = [$type, $this_click, $click_timestamp, $url].join()
        $user_data += $data + ";";
    });
}

function all_questions_answered() {
    var i = 0;
    var c = $(".ion-android-radio-button-on").each(function() {
        i += 1;
    });
    //return true; // enable this for not enforcing answer all questions to proceed.
    return (i == 6);
}

function create_end_session() {
    $("#end_session").bind('click', function() {
        var r = confirm("Are you sure to end your session?");
        if (r == true) {
            $(window).off("beforeunload");
            window.location.href = '/post_survey';
        } 
    })
}

/*
    This function defines the behavior of the next button in record linkage page:
    1. disable this button
    2. post the user data to server
    3. redirect to next page
*/
$(function() {
    $('#button_next_rl').bind('click', function() {
        if( !all_questions_answered() ) {
            alert("Please answer all questions to continue.");
        }
        else {
            $('#button_next_rl').attr("disabled", "disabled");
            get_summitted_answers();
            post($SCRIPT_ROOT+'/save_data', $user_data, "post");
            $(window).off("beforeunload");
            window.location.href = $NEXT_URL;
        }
        return false;
    });

    $('#save_exit').bind('click', function() {
        get_summitted_answers();
        post($SCRIPT_ROOT+'/save_exit', $user_data, "post");
        $(window).off("beforeunload");
        window.location.href = $PROJ_URL;
        return false;
    });
});
