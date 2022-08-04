$("#send_button").on("click", function(){
    var message = $("#ticket_message").val();

    $("#loader").html('<img src="/static/images/loader.gif">');

    var token = window.localStorage.getItem('ACCESS_TOKEN');
    $.ajax({
        url: "/api/tickets/new",
        headers: {"Authorization": "Token "+token},
        data: {ticket_message: message},
        type: "POST",
        success: function() {
            console.log("success");
        }
    });
});
$("#cancel_button").on("click", function(){
    window.location.href = prev_url;
});
