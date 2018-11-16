$( document ).ready(function() {
    $('.custom-file-input').on('change',function(){
        var fileName = $(this).val();
        fileName = fileName.split("\\");
        fileName = fileName[fileName.length-1]
        $(this).next().addClass("selected").html(fileName);
    })

    $("#project_name").on('change', function(){
        $("#project_name-error").html("");
    })

    $("#kapr").on('change', function(){
        $("#kapr-error").html("");
    })

    $("#blocking").on('change', function(){
        $("#blocking-error").html("");
    })

    $("#data1").on('change', function(){
        $("#data1-error").html("");
    })

    $("#data2").on('change', function(){
        $("#data2-error").html("");
    })

    $("#data3").on('change', function(){
        $("#data3-error").html("");
    })
});




function reset_form_error() {
    $("#project_name-error").html("");
    $("#kapr-error").html("");
    $("#blocking-error").html("");
    $("#data1-error").html("");
    $("#data2-error").html("");
    $("#data3-error").html("");
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
    value = $("#data3").val();
    if(value == null || value == "") {
        $("#data3-error").html("Please select a file to upload.");
        ret = false;
    }
    return ret;
}