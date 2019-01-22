 /*
    Author: Yumei Li
    Date: 12/23/2017
    Modified by Qinbo Li
    Requirement: jquery-3.2.1
    This file makes the elements in the file clickable
*/

function pround(number, precision) {
    var factor = Math.pow(10, precision);
    var ret = Math.round(number * factor) / factor;
    if(number > 0 && ret < 0.01) {
        return 0.01;
    }
    return ret;
}

function get_response(clicked_object) {
    var mode_info = clicked_object.getAttribute("mode");
    var id1 = clicked_object.children[0].id;
    var id2 = clicked_object.children[2].id;

    return {
        "id1": id1,
        "id2": id2,
        "mode": mode_info
    };
}

function get_response2(clicked_object1, clicked_object2) {
    var mode_info = clicked_object1.getAttribute("mode");
    var id1 = clicked_object1.children[0].id;
    var id2 = clicked_object1.children[2].id;
    var id3 = clicked_object2.children[0].id;
    var id4 = clicked_object2.children[2].id;

    return {
        "id1": id1,
        "id2": id2,
        "id3": id3,
        "id4": id4,
        "mode": mode_info
    };
}

function get_cell_ajax(current_cell) {
    $.fn.extend({
        animateCss: function (animationName, callback) {
            var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            this.addClass('animated ' + animationName).one(animationEnd, function() {
                $(this).removeClass('animated ' + animationName);
                if (callback) {
                    callback();
                }
            });
            return this;
        }
    });

    $.getJSON($SCRIPT_ROOT + '/get_cell', get_response(current_cell), function(data) {
        if( data.result != "success") {
            // failed, do nothing.
        }
        else if(data.value1 && data.value2 && data.mode) {
            current_cell.classList.add("animated");
            current_cell.classList.add("fadeIn");
            window.setTimeout( function(){
                current_cell.classList.remove("animated");
                current_cell.classList.remove("fadeIn");
            }, 200);

            current_cell.children[0].innerHTML = data.value1;
            current_cell.children[2].innerHTML = data.value2;
            current_cell.setAttribute("mode", data.mode);
            if(data.mode == "full") {
                current_cell.classList.remove("clickable_cell");
            }
            $KAPR = data.KAPR;
            
            //var bar_style = 'width:' + data.cdp + '%';
            //$("#character-disclosed-bar").attr("style", bar_style);
            //$("#character-disclosed-value").html(data.cdp + "%")

            var bar_style2 = 'width:' + data.KAPR + '%';
            $("#privacy-risk-bar").attr("style", bar_style2);
            $("#privacy-risk-value").html(pround(data.KAPR,1) + "%")
            
            $("#privacy-risk-delta").attr("style", 'width: 0%');
            $("#privacy-risk-delta-value").html(" ")

            for(var i = 0; i < 6; i+=1) {
                var id = data.new_delta[i][0];
                var new_delta_value = data.new_delta[i][1];
                $DELTA[id] = new_delta_value;
            }

            // save the user click data
        }
    });
}

function get_big_cell_ajax(current_cell1, current_cell2) {
    $.fn.extend({
        animateCss: function (animationName, callback) {
            var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            this.addClass('animated ' + animationName).one(animationEnd, function() {
                $(this).removeClass('animated ' + animationName);
                if (callback) {
                  callback();
                }
            });
            return this;
        }
    });

    $.getJSON($SCRIPT_ROOT + '/get_big_cell', get_response2(current_cell1, current_cell2), function(data) {
        if( data.result != "success") {
            return false;
        }
        else if(data.value1 && data.value2 && data.mode) {
            current_cell1.classList.add("animated");
            current_cell1.classList.add("fadeIn");
            current_cell2.classList.add("animated");
            current_cell2.classList.add("fadeIn");
            window.setTimeout( function(){
                current_cell1.classList.remove("animated");
                current_cell1.classList.remove("fadeIn");
                current_cell2.classList.remove("animated");
                current_cell2.classList.remove("fadeIn");
            }, 200);

            current_cell1.children[0].innerHTML = data.value1;
            current_cell1.children[2].innerHTML = data.value2;
            current_cell1.setAttribute("mode", data.mode);
            current_cell2.children[0].innerHTML = data.value3;
            current_cell2.children[2].innerHTML = data.value4;
            current_cell2.setAttribute("mode", data.mode);

            if(data.mode == "full") {
                current_cell1.parentElement.classList.remove("clickable_big_cell");
            }

            $KAPR = data.KAPR;
            
            var bar_style2 = 'width:' + data.KAPR + '%';
            $("#privacy-risk-bar").attr("style", bar_style2);
            $("#privacy-risk-value").html(pround(data.KAPR,1) + "%")
            
            $("#privacy-risk-delta").attr("style", 'width: 0%');
            $("#privacy-risk-delta-value").html(" ")

            for(var i = 0; i < 6; i+=1) {
                var id = data.new_delta[i][0];
                var new_delta_value = data.new_delta[i][1];
                $DELTA[id] = new_delta_value;
            }

            // save the user click data
        }
        return true;
    });
}

function make_cell_clickable() {
    // mark the double missing cell as unclickable
    $('.clickable_cell').each(function() {
        if( this.children[0].innerHTML.indexOf('missing') != -1 && this.children[2].innerHTML.indexOf('missing') != -1 ) {
            this.classList.remove("clickable_cell");
        }
    });

    // bind the clickable cell to ajax openning cell action
    $('.clickable_cell').bind('click', function() {
        var current_cell = this;
        if(current_cell.getAttribute("mode") != "full") {
            get_cell_ajax(current_cell);
        }

        // save the user click data
        return false;
    });

    // big cell is the name swap cell
    $('.clickable_big_cell').bind('click', function() {
        var first_name_cell = this.children[0];
        var last_name_cell = this.children[2];
        if(first_name_cell.getAttribute("mode") != "full") {
            flag = get_big_cell_ajax(first_name_cell, last_name_cell);
        }

        // save the user click data
        return false;
    });
}

function remove_clickable_cells() {
    // remove clickable_cell class on the whole page.
    $('.clickable_cell').each(function() {
        this.classList.remove("clickable_cell");
    });
    $('.clickable_big_cell').each(function() {
        this.classList.remove("clickable_big_cell");
    });
}

function refresh_delta() {
    $('.clickable_cell').hover(function() {
        if(this.classList.contains('clickable_cell')) {
            var id1 = this.children[0].getAttribute("id");
            var d = $DELTA[id1];

            // if there is a budget limit, then check if this cell goes over the limit
            if( typeof $KAPR_LIMIT !== 'undefined' && $KAPR_LIMIT >= 0 && $KAPR + d > $KAPR_LIMIT) {
                $(this).css('cursor', 'not-allowed');
                // this.classList.remove("clickable_cell");
            }
            var bar_style = 'width:' + pround(d,2) + '%';
            $("#privacy-risk-delta").attr("style", bar_style);
            $("#privacy-risk-delta-value").html(" + " + pround(d,2) + "%");
        }
    }, function() {
        $("#privacy-risk-delta").attr("style", 'width: 0%');
        $("#privacy-risk-delta-value").html(" ")
    });

    $('.clickable_big_cell').hover(function() {
        if(this.classList.contains('clickable_big_cell')) {
            var id1 = this.children[0].children[0].getAttribute("id");
            var id2 = this.children[2].children[0].getAttribute("id");
            var d = $DELTA[id1] + $DELTA[id2];
            // if there is a budget limit, then check if this cell goes over the limit
            if( typeof $KAPR_LIMIT !== 'undefined' && $KAPR_LIMIT >= 0 && $KAPR + d > $KAPR_LIMIT) {
                $(this).css('cursor', 'not-allowed');
                // $(this).classList.remove("clickable_big_cell");
            }
            var bar_style = 'width:' + pround(d,2) + '%';
            $("#privacy-risk-delta").attr("style", bar_style);
            $("#privacy-risk-delta-value").html(" + " + pround(d,2) + "%");
        }
    }, function() {
        $("#privacy-risk-delta").attr("style", 'width: 0%');
        $("#privacy-risk-delta-value").html(" ")
    });
}

$(function() {
    if(typeof $USTUDY_MODE === 'undefined' || $USTUDY_MODE != 1) {
        make_cell_clickable();
    }
    else {
        remove_clickable_cells();
    }
    refresh_delta();
});

