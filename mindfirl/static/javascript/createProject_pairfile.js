var assignee_list = [1];

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

    add_assignee();
});

function add_assignee() {
    var next = 1;
        
        $("#add-assignee").click(function(e){
            e.preventDefault();
            next = next + 1;
            var newIn = `<div id="assignee_${next}">
                            <label class="" for="assignto">Assign to</label>
                            <select class="form-control selectpicker" data-live-search="ture" id="assignto_${next}" name="assignto2">
                                ${option_str}
                            </select>
                            <div class="form-group" style="margin-bottom: 0">
                                Privacy budget:
                                <input class="form-control" type="number" placeholder="Privacy budget (%)" step="any" min="0" max="100" name="privacy_budget_${next}" id="kapr_${next}" value="">
                                <div class="form-error" id="kapr_${next}-error"></div>
                                Assignment percentage:
                                <input class="form-control" type="number" placeholder="Assignment percentage (%)" step="1" min="0" max="100" name="percentage_${next}" id="percentage_${next}" value="">
                                <div class="form-error" id="percentage_${next}-error"></div>
                                <label><input type="checkbox" id="full_${next}" name="full_${next}" value="full">Fully open</label><br>
                            </div>
                            <div class="remove-me" id="remove-${next}" style="color: red; cursor: pointer; margin-top: 0px; margin-bottom: 16px">
                                - <span style="text-decoration: underline;">Remove this</span>
                            </div>
                        </div>
                        `;
            var newInput = $(newIn);

            var addto = "#assignee_" + assignee_list[assignee_list.length-1];
            $(addto).after(newInput);
            assignee_list.push(next);

            $('.selectpicker').selectpicker();

            $('.remove-me').click(function(e){
                e.preventDefault();
                var num = this.id.split('-')[1]
                var assignee_id = "#assignee_" + num;
                $(assignee_id).remove();

                var index = assignee_list.indexOf(parseInt(num));
                if (index !== -1) assignee_list.splice(index, 1);
            }); 
        });
}

function check_assignee() {
    var ret = true;

    for(i = 0; i < assignee_list.length; i++) {
        var idx = assignee_list[i];
        var assignee = $('#assignto_'+idx).val();
        var kapr = $('#kapr_'+idx).val();
        var percentage = $('#percentage_'+idx).val();
        if(assignee == null || assignee == "") {
            ret = false;
        }
        if(kapr == null || kapr == "") {
            $("#kapr_"+idx+"-error").html("Please enter a value.");
            $("#kapr_"+idx).on('change', function(){
                $("#kapr_"+idx+"-error").html("");
            });
            ret = false;
        }
        if(percentage == null || percentage == "") {
            $("#percentage_"+idx+"-error").html("Please enter a value.");
            $("#percentage_"+idx).on('change', function(){
                $("#percentage_"+idx+"-error").html("");
            });
            ret = false;
        }
    }

    return ret;
}

function encode_assignee() {
    var total_percentage = 0;
    var encoded_assignee = "";
    for(i = 0; i < assignee_list.length; i++) {
        var idx = assignee_list[i];
        var assignee = $('#assignto_'+idx).val();
        var kapr = $('#kapr_'+idx).val();
        var percentage = $('#percentage_'+idx).val();
        var full = $('#full_'+idx).is(':checked');

        encoded_assignee += (assignee + ',' + kapr + ',' + percentage + ',' + full + ';');

        total_percentage += parseInt(percentage);
    }
    $("#assignee_area").html(encoded_assignee);

    //if(total_percentage == 100)
    //    return true;
    //$("#percentage_1-error").html("Percentage must add up to 100.");
    return true;
}


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
    if(value.indexOf(" ") != -1) {
        $("#project_name-error").html("No space in project name.");
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

    if(check_assignee() == false) {
        ret = false;
    }
    return ret && encode_assignee();
}