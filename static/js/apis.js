
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
    var role = $("#role").val();

    $.post("/api/user/register", {role:role, username: user, password: password, firstname, lastname}, function (response) {
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

$("#new_ticket_button").on("click", function(){
    var message = $("#ticket_message").val();

    $.post("/api/tickets/new", {ticket_message: message}, function (response) {
        handleResponse("/videos/list", response, function(r){}, "نام کاربری یا رمز عبور اشتباه است");
    });
});

$("#cancel_new_ticket_button").on("click", function(){
    window.location.href = "/tickets/my_tickets";
});

$("#new_comment_button").on("click", function(){
    var message = $("#comment_message").val();
    var video_id = $("#video_id_input").val();
    $.post("/api/comments/new", {videoId: video_id, message}, function (response) {
        handleResponse(window.location.href, response, function (r) {}, 'مشکلی در نظر دادن پیش آمد.')
    });
});
$("#like_video").on("click", function(){
    console.log("Dwf");
    var video_id = $("#video_id_input").val();
    console.log(video_id);
    $.post("/api/like", {videoId: video_id}, function (response) {
        handleResponse(window.location.href, response, function (r) {}, 'مشکلی پیش آمد.')
    });
});
$("#dislike_video").on("click", function(){
    var video_id = $("#video_id_input").val();
    $.post("/api/dislike", {videoId: video_id}, function (response) {
        handleResponse(window.location.href, response, function (r) {}, 'مشکلی پیش آمد.')
    });
});

$("#delete_video").on("click", function(){
    var video_id = $("#video_id_input").val();
    $.post("/videos/s/"+video_id+"/delete", {}, function (response) {
        handleResponse("/videos/list", response, function (r) {}, 'مشکلی پیش آمد.')
    });
});

$("#sensitive_video").on("click", function(){
    var video_id = $("#video_id_input").val();
    $.post("/videos/s/"+video_id+"/sensitive", {}, function (response) {
        handleResponse(window.location.href, response, function (r) {}, 'مشکلی پیش آمد.')
    });
});

$("#add_message_button").on("click", function(){
    var message = $("#new_ticket_message").val();
    var ticket_id = $("#ticket_id").val();
    var username = $("#username").val();
     window.location.href="/videos/list"
    $.post("/api/tickets/add_message", {ticket_id: ticket_id, username: username, ticket_message:message}, function (response) {
        handleResponse("/videos/list", response, function (r) {}, "مشکلی در اضافه کردن پیام پیش آمد.");
    });
});

$("#change_state_button").on("click", function(){
    var select_value = $("#select_state").val();
    var ticket_id = $("#ticket_id").val();
    $.post("/api/tickets/change_state", {ticket_id: ticket_id, new_state:select_value}, function (response) {
        handleResponse("/videos/list", response, function (r) {}, 'مشکلی در تغییر وضعیت به وجود آمد.')});
});