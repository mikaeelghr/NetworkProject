from flask import request, Flask, make_response
from flask import render_template
from flask import redirect, url_for
import json

from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from service.auth import must_be_user, AuthService, must_be_authenticated, must_be_admin, must_be_staff, \
    must_be_supervisor, authenticate_if_token_exists
from service.user import UserService
from service.video import VideoService
from service.ticket import TicketService


def add_routes(app: Flask):
    @app.route('/')
    @app.route('/login')
    @authenticate_if_token_exists
    def login_page():
        return render_template("login.html", authenticated=request.authenticated)

    @app.route('/register')
    @authenticate_if_token_exists
    def register_page():
        return render_template("register.html", authenticated=request.authenticated)

    @app.route('/videos/list')
    @authenticate_if_token_exists
    def get_videos():
        show_upload_btn = None
        if request.authenticated:
            show_upload_btn = request.user.role == "USER"
        return render_template("all_video.html", videos=VideoService.get_list(), show_upload_btn=show_upload_btn,
                               authenticated=request.authenticated)

    @app.route('/api/user/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        user = UserService.login(username, password)
        if user is None:
            return json.dumps({'success': False})
        access_token = AuthService.generateToken(user)

        response = make_response(json.dumps({'success': True, 'token': access_token}))
        response.set_cookie("TOKEN", access_token, httponly=True)
        return response

    @app.route('/logout', methods=['GET'])
    def logout():
        response = make_response(redirect("/login"))
        response.set_cookie("TOKEN", "", httponly=True)
        return response

    @app.route('/api/user/register', methods=['POST'])
    def register():
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        try:
            user = UserService.register(username, password, firstname, lastname)
        except DuplicateKeyError:
            return json.dumps({'success': False, "message": "نام کاربری تکراری است"})
        except ValidationError:
            return json.dumps({'success': False, "message": "مقادیر را درست وارد کنید"})
        access_token = AuthService.generateToken(user)
        response = make_response(json.dumps({'success': True, 'token': access_token}))
        response.set_cookie("TOKEN", access_token, httponly=True)
        return response

    @app.route('/videos/upload/', methods=['GET', 'POST'])
    @must_be_user
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
                                   success_desc="ویدیو با موفیت آپلود شد", authenticated=request.authenticated)
        else:
            return render_template("add_video.html", form_all_tags=['سرگرمی', 'آموزشی'],
                                   authenticated=request.authenticated)

    @app.route('/videos/s/<video_id>', methods=['GET'])
    @authenticate_if_token_exists
    def get_stream_of_user(video_id):
        video = VideoService.get(video_id)
        if video is None:
            return json.dumps({"error": "file not found"})
        user_id = None
        if request.authenticated:
            user_id = str(request.user._id)
        return render_template("show_video.html", video=video, user_id=user_id, authenticated=request.authenticated)

    @app.route('/tickets/new')
    @authenticate_if_token_exists
    def tickets():
        return render_template("new_ticket.html", authenticated=request.authenticated)

    @app.route('/api/tickets/new', methods=['POST'])
    @must_be_authenticated
    def new_ticket():
        user_id = request.user._id
        ticket_message = request.user.username + ': ' + request.form['ticket_message']
        TicketService.create_ticket(user_id=user_id, user_role=request.user.role, message=ticket_message)
        return json.dumps({'success': True})

    @app.route('/tickets/<ticket_id>', methods=['GET'])
    @authenticate_if_token_exists
    def show_ticket(ticket_id):
        ticket = TicketService.get_ticket_by_id(ticket_id)
        return render_template('ticket.html', ticket=ticket, user=request.user, authenticated=request.authenticated)

    @app.route('/api/tickets/add_message', methods=['POST'])
    def add_message():
        ticket_id = request.form['ticket_id']
        username = request.form['username']
        ticket_message = request.form['ticket_message']
        TicketService.add_message(ticket_id, username, ticket_message)
        return json.dumps({'success': True})

    @app.route('/api/tickets/change_state', methods=['POST'])
    def change_state():
        ticket_id = request.form['ticket_id']
        new_state = request.form['new_state']
        TicketService.change_state(ticket_id, new_state)
        return json.dumps({'success': True})

    @app.route('/api/comments/new', methods=['POST'])
    @must_be_authenticated
    def new_comment():
        video_id = request.form['videoId']
        message = request.form['message']
        user_id = str(request.user._id)
        VideoService.add_comment(video_id, user_id, message)
        return json.dumps({'success': True})

    @app.route('/api/like', methods=['POST'])
    @must_be_authenticated
    def like_video():
        video_id = request.form['videoId']
        user_id = str(request.user._id)
        VideoService.like(video_id, user_id)
        return json.dumps({'success': True})

    @app.route('/api/dislike', methods=['POST'])
    @must_be_authenticated
    def dislike_video():
        video_id = request.form['videoId']
        user_id = str(request.user._id)
        VideoService.dislike(video_id, user_id)
        return json.dumps({'success': True})

    @app.route('/tickets/my_tickets', methods=['GET'])
    @must_be_authenticated
    def my_tickets():
        tickets = TicketService.get_user_tickets(request.user._id)
        return render_template('my_tickets.html', tickets=tickets, user_id=request.user._id, authenticated=request.authenticated)

    @app.route("/tickets/assigned_tickets", methods=['GET'])
    @must_be_supervisor
    def assigned_tickets():
        tickets = TicketService.get_assigned_tickets(request.user._id)
        return render_template('my_tickets.html', tickets=tickets, user_id=request.user._id, authenticated=request.authenticated)
