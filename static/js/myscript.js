$("#loginbtn").on("click", function(){
    var user = $("#username").val();
    var password = $("#password").val();

    $("#loader").html('<img src="/static/images/loader.gif">');

    $.post("/api/user/login", {username: user, password: password}, function (response) {

      $("#loader").html('');
      var response = JSON.parse(response);

      if (response.success) {
        window.localStorage.setItem('ACCESS_TOKEN', response.token);
        window.location.href = "/tickets/new";
      }
      else {
         $("#loader").html('<p class="alert alert-danger">نام کاربری یا رمز عبور اشتباه است</p>');
      }
    });
});

$("#logoutbtn").on("click", function(){
    $.post("/api/user/logout", {action: 'logout'}, function (response) {
    });
});

$("#likeBtn").on("click", function(){
    var token = window.localStorage.getItem('ACCESS_TOKEN');
    $.ajax({
        url: "/video/felan/like",
        headers: {"Authorization": "Token "+token},
        data: {
            // body
        },
        type: "POST",
        success: function() {
            // felan
        }
    });

});

$("#unlikeBtn").on("click", function(){
    // felan
});
