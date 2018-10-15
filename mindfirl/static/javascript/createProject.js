$( document ).ready(function() {
    $('.custom-file-input').on('change',function(){
        var fileName = $(this).val();
        fileName = fileName.split("\\");
        fileName = fileName[fileName.length-1]
        $(this).next().addClass("selected").html(fileName);
    })

});




function reset_form_error() {
    $("#project_name-error").html("");
    $("#kapr-error").html("");
    $("#blocking-error").html("");
    $("#data1-error").html("");
    $("#data2-error").html("");
}

function check_form(thisform) {
    reset_form_error();

    var ret = true;
    var value = $("#project_name").val();
    if(value == null || value == "") {
        $("#project_name-error").html("Please enter a value.");
        ret = false;
    }
    value = $("#kapr").val();
    if(value == null || value == "") {
        $("#kapr-error").html("Please enter a value.");
        ret = false;
    }
    value = $("#blocking").val();
    if(value == null || value == "") {
        $("#blocking-error").html("Please select a blocking attribute.");
        ret = false;
    }
    value = $("#data1").val();
    if(value == null || value == "") {
        $("#data1-error").html("Please select a file to upload.");
        ret = false;
    }
    value = $("#data2").val();
    if(value == null || value == "") {
        $("#data2-error").html("Please select a file to upload.");
        ret = false;
    }
    return ret;
}