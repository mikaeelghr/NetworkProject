$("#loginbtn").on("click", function(){
    var user = $("#username").val();
    var password = $("#password").val();

    $.post("/api/user/login", {username: user, password: password}, function (response) {

      $("#loader").html('');
      var response = JSON.parse(response);

      if (response.success) {
        window.localStorage.setItem('ACCESS_TOKEN', response.token);
        window.location.href = "/tickets/new";
      }
      else {
         $("#error_desc").html('<p class="alert alert-danger">نام کاربری یا رمز عبور اشتباه است</p>');
      }
    });
});

$("#registerbtn").on("click", function(){
    var user = $("#username").val();
    var password = $("#password").val();
    var firstname = $("#firstname").val();
    var lastname = $("#lastname").val();

    $.post("/api/user/register", {username: user, password: password, firstname, lastname}, function (response) {

      $("#loader").html('');
      var response = JSON.parse(response);

      if (response.success) {
        window.localStorage.setItem('ACCESS_TOKEN', response.token);
        window.location.href = "/tickets/new";
        $("#error_desc").html('<p class="success">ثبت نام انجام شد</p>');
      }
      else {
         $("#error_desc").html('<p class="alert alert-danger">مشکلی پیش آمده است</p>');
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
