
function handleResponse(successUrl, response, successFunc, defaultMessage) {
    var response = JSON.parse(response);

    if (response.success) {
        successFunc(response);
        window.location.href = successUrl;
    }
    else {
        var message = response.message || defaultMessage || "مشکلی پیش آمده است";
        $("#error_desc").html('<p class="alert alert-danger">'+message+'</p>');
    }
}

$("#loginbtn").on("click", function(){
    var user = $("#username").val();
    var password = $("#password").val();

    $.post("/api/user/login", {username: user, password: password}, function (response) {
        handleResponse("/videos/list", response, function ({token}) { window.localStorage.setItem('ACCESS_TOKEN', token) }, "نام کاربری یا رمز عبور اشتباه است");
    });
});

$("#registerbtn").on("click", function(){
    var user = $("#username").val();
    var password = $("#password").val();
    var firstname = $("#firstname").val();
    var lastname = $("#lastname").val();

    $.post("/api/user/register", {username: user, password: password, firstname, lastname}, function (response) {
        handleResponse("/videos/list", response, function ({token}) { window.localStorage.setItem('ACCESS_TOKEN', token) });
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

$("#loginRedirectBtn").on("click", function(){
    window.location.href = "/login";
});

$("#registerRedirectBtn").on("click", function(){
    window.location.href = "/register";
});

$("#send_button").on("click", function(){
    var message = $("#ticket_message").val();

    $.post("/api/tickets/new", {ticket_message: message}, function (response) {
        handleResponse("/videos/list", response, function(r){}, "نام کاربری یا رمز عبور اشتباه است");
    });
});

$("#cancel_button").on("click", function(){
    window.location.href = prev_url;
});
