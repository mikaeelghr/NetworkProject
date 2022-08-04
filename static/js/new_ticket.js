$("#send_button").on("click", function(){
    var message = $("#ticket_message").val();

    $("#loader").html('<img src="/static/images/loader.gif">');

    $.post("/tickets/new_ticket", {ticket_message: ticket_message}, function (response) {

      $("#loader").html('');
      var response = JSON.parse(response);

      if (response.success) {
//        window.localStorage.setItem('ACCESS_TOKEN', response.token);
//        window.location.href = nextURL;
      }
      else {
         $("#loader").html('<p class="alert alert-danger">An error has been occurred during the creation of ticket </p>');
      }
    });
});
$("#cancel_button").on("click", function(){
    window.location.href = prev_url;
});
