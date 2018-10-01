$(function() {
    $(".confirm-link").bind('click', function() {
        address = this.getAttribute("address");
        message = this.getAttribute("message");

        r = confirm(message);
        if(r == true) {
            window.location.href = address;
        }
    });
});