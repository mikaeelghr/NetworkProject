$("#loginbtn").on("click", function(){
    var user = $("#username").val();
    var password = $("#password").val();
    var nextURL = $("#nextURL").val();

    $("#loader").html('<img src="/static/images/loader.gif">');

    $.post("/user/login", {username: user, password: password}, function (response) {

      $("#loader").html('');
      var response = JSON.parse(response);

      if (response.success) {
        window.localStorage.setItem('ACCESS_TOKEN', response.token);
        window.location.href = nextURL;
      }
      else {
         $("#loader").html('<p class="alert alert-danger">نام کاربری یا رمز عبور اشتباه است</p>');
      }
    });
});

$("#logoutbtn").on("click", function(){
    $.post("/user/logout", {action: 'logout'}, function (response) {
        window.location.href = "index.php";
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
