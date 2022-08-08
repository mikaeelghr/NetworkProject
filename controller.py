from flask import request, Flask, make_response
from flask import render_template
from flask import redirect, url_for
import json

from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import RequestEntityTooLarge

from service.auth import must_be_user, AuthService, must_be_authenticated, must_be_admin, must_be_staff, \
    must_be_supervisor, ddos_checker, authenticate_if_token_exists
from service.user import UserService
from service.video import VideoService
from service.ticket import TicketService


def add_routes(app: Flask):
    @app.route('/')
    @app.route('/login')
    @authenticate_if_token_exists
    @ddos_checker
    def login_page():
        return render_template("login.html", request=request)

    @app.route('/register')
    @authenticate_if_token_exists
    @ddos_checker
    def register_page():
        return render_template("register.html", request=request)

    @app.errorhandler(413)
    @app.errorhandler(RequestEntityTooLarge)
    def request_entity_too_large(error):
        return 'File Too Large', 413

    @app.route('/videos/list')
    @authenticate_if_token_exists
    @ddos_checker
    def get_videos():
        show_upload_btn = None
        if request.authenticated:
            show_upload_btn = request.user.role == "USER"
        return render_template("all_video.html", videos=VideoService.get_list(), show_upload_btn=show_upload_btn,
                               request=request)

    @app.route('/api/user/login', methods=['POST'])
    @ddos_checker
    def login():
        username = request.form['username']
        password = request.form['password']

        user = UserService.login(username, password)
        if user is None:
            return json.dumps({'success': False})
        # ADD THIS FOR STAFF
        if user.verified == False:
            return json.dumps({'success': False})

        access_token = AuthService.generateToken(user)
        response = make_response(json.dumps({'success': True, 'token': access_token}))
        response.set_cookie("TOKEN", access_token, httponly=True)
        return response

    @app.route('/logout', methods=['GET'])
    @ddos_checker
    def logout():
        response = make_response(redirect("/login"))
        response.set_cookie("TOKEN", "", httponly=True)
        return response

    @app.route('/api/user/register', methods=['POST'])
    @ddos_checker
    def register():
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        # ADD THIS FOR STAFF
        role = request.form['role']
        verified = True
        if role == 'STAFF': verified = False

        try:
            user = UserService.register(username, password, firstname, lastname, role, verified)
        except DuplicateKeyError:
            return json.dumps({'success': False, "message": "نام کاربری تکراری است"})
        except ValidationError:
            return json.dumps({'success': False, "message": "مقادیر را درست وارد کنید"})

        # ADD THIS FOR STAFF
        if role == 'STAFF':
            return json.dumps({'success': False, "message": "اکانت شما باید تایید شود."})
        access_token = AuthService.generateToken(user)
        response = make_response(json.dumps({'success': True, 'token': access_token}))
        response.set_cookie("TOKEN", access_token, httponly=True)
        return response

    @app.route('/staff/verification', methods=['GET'])
    @must_be_admin
    @ddos_checker
    def get_unverified_staffs():
        unverified_staffs = UserService.get_unverified_staffs()
        return render_template("verify_staff.html", staffs=unverified_staffs, request=request)

    @app.route('/staff/verify/<staff_id>', methods=['GET'])
    @must_be_admin
    @ddos_checker
    def verify_staff(staff_id):
        UserService.verify_staff(staff_id)
        return get_unverified_staffs()

    @app.route('/videos/upload/', methods=['GET', 'POST'])
    @must_be_user
    @ddos_checker
    def upload_video():
        if request.method == 'POST':
            user_id = request.user._id
            if 'file' not in request.files or request.files['file'] == '':
                return redirect(request.url)
            file = request.files['file']
            name = request.form['name']
            title = request.form['title']
            try:
                VideoService.add(str(user_id), name, title, file)
            except Exception:
                return json.dumps({"success": False, "error": "invalid file type"})
            return render_template("add_video.html", form_all_tags=['سرگرمی', 'آموزشی'], success=True,
                                   success_desc="ویدیو با موفیت آپلود شد", request=request)
        else:
            return render_template("add_video.html", form_all_tags=['سرگرمی', 'آموزشی'],
                                   request=request)

    @app.route('/videos/s/<video_id>', methods=['GET'])
    @authenticate_if_token_exists
    @ddos_checker
    def get_stream_of_user(video_id):
        video = VideoService.get(video_id)
        if video is None:
            return json.dumps({"error": "file not found"})
        user_id = None
        if request.authenticated:
            user_id = str(request.user._id)
        return render_template("show_video.html", video=video, user_id=user_id, request=request)

    @app.route('/videos/s/<video_id>/delete', methods=['POST'])
    @must_be_staff
    @ddos_checker
    def delete_video(video_id):
        video = VideoService.get(video_id)
        if video is None:
            return json.dumps({"error": "file not found"})
        VideoService.delete(video_id)
        return json.dumps({'success': True})

    @app.route('/videos/s/<video_id>/sensitive', methods=['POST'])
    @must_be_staff
    @ddos_checker
    def sensitive_video(video_id):
        video = VideoService.get(video_id)
        if video is None:
            return json.dumps({"error": "file not found"})
        VideoService.add_tag(video_id, "ویدیو به عنوان خطرناک برچسب گذاری شده است")
        return json.dumps({'success': True})

    @app.route('/tickets/new')
    @authenticate_if_token_exists
    @ddos_checker
    def tickets():
        return render_template("new_ticket.html", request=request)

    @app.route('/api/tickets/new', methods=['POST'])
    @must_be_authenticated
    def new_ticket():
        user_id = request.user._id
        ticket_message = request.user.username + ': ' + request.form['ticket_message']
        TicketService.create_ticket(user_id=user_id, user_role=request.user.role, message=ticket_message)
        return json.dumps({'success': True})

    @app.route('/tickets/<ticket_id>', methods=['GET'])
    @authenticate_if_token_exists
    @ddos_checker
    def show_ticket(ticket_id):
        ticket = TicketService.get_ticket_by_id(ticket_id)
        return render_template('ticket.html', ticket=ticket, user=request.user, request=request)

    @app.route('/api/tickets/add_message', methods=['POST'])
    @ddos_checker
    def add_message():
        ticket_id = request.form['ticket_id']
        username = request.form['username']
        ticket_message = request.form['ticket_message']
        TicketService.add_message(ticket_id, username, ticket_message)
        return json.dumps({'success': True})

    @app.route('/api/tickets/change_state', methods=['POST'])
    @ddos_checker
    def change_state():
        ticket_id = request.form['ticket_id']
        new_state = request.form['new_state']
        TicketService.change_state(ticket_id, new_state)
        return json.dumps({'success': True})

    @app.route('/api/comments/new', methods=['POST'])
    @must_be_authenticated
    @ddos_checker
    def new_comment():
        video_id = request.form['videoId']
        message = request.form['message']
        user_id = str(request.user._id)
        VideoService.add_comment(video_id, user_id, message)
        return json.dumps({'success': True})

    @app.route('/api/like', methods=['POST'])
    @must_be_authenticated
    @ddos_checker
    def like_video():
        video_id = request.form['videoId']
        user_id = str(request.user._id)
        VideoService.like(video_id, user_id)
        return json.dumps({'success': True})

    @app.route('/api/dislike', methods=['POST'])
    @must_be_authenticated
    @ddos_checker
    def dislike_video():
        video_id = request.form['videoId']
        user_id = str(request.user._id)
        VideoService.dislike(video_id, user_id)
        return json.dumps({'success': True})

    @app.route('/tickets/my_tickets', methods=['GET'])
    @must_be_authenticated
    @ddos_checker
    def my_tickets():
        tickets = TicketService.get_user_tickets(request.user._id)
        return render_template('my_tickets.html', assigned_page=False, tickets=tickets, user_id=request.user._id,
                               request=request)

    @app.route("/tickets/assigned_tickets", methods=['GET'])
    @must_be_supervisor
    @ddos_checker
    def assigned_tickets():
        tickets = TicketService.get_assigned_tickets(request.user._id)
        return render_template('my_tickets.html', assigned_page=True, tickets=tickets, user_id=request.user._id,
                               request=request)

    @app.route("/tickets/get_ticket", methods=['GET'])
    @must_be_staff
    @ddos_checker
    def get_ticket():
        TicketService.assign_ticket(request.user)
        return redirect(url_for("assigned_tickets"))
