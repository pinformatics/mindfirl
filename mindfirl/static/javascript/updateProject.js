function reset_form_error() {
    $("#project_name-error").html("");
    $("#kapr-error").html("");
}

function check_form(thisform) {
    reset_form_error();

    var ret = true;
    var value = $("#project_name").val();
    if(value == null || value == "") {
        $("#project_name-error").html("Please enter a value.");
        ret = false;
    }
    if(value.indexOf(" ") != -1) {
        $("#project_name-error").html("No space in project name.");
        ret = false;
    }
    value = $("#kapr").val();
    if(value == null || value == "") {
        $("#kapr-error").html("Please enter a value.");
        ret = false;
    }
    return ret;
}