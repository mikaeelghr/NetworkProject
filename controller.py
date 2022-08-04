from flask import request, Flask, make_response
from flask import render_template
from flask import redirect, url_for
import json

from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from service.token import must_be_user, TokenService
from service.user import UserService
from service.video import VideoService
from service.ticket import TicketService


def add_routes(app: Flask):
    @app.route('/')
    @app.route('/login')
    def login_page():
        return render_template("login.html")

    @app.route('/register')
    def register_page():
        return render_template("register.html", user=None)

    @app.route('/videos/list')
    def get_videos():
        return render_template("all_video.html", videos=VideoService.get_list())

    @app.route('/api/user/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        user = UserService.login(username, password)
        if user is None:
            return json.dumps({'success': False})
        access_token = TokenService.generateToken(user)

        response = make_response(json.dumps({'success': True, 'token': access_token}))
        response.set_cookie("TOKEN", access_token, httponly=True)
        return response

    @app.route('/logout', methods=['GET'])
    def logout():
        response = make_response(redirect("/login"))
        response.set_cookie("TOKEN", "", httponly=True)
        return response

    @app.route('/api/user/register', methods=['POST'])
    # @must_be_admin
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
        access_token = TokenService.generateToken(user)
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
            VideoService.add(str(user_id), name, title, file)
            return render_template("add_video.html", form_all_tags=['سرگرمی', 'آموزشی'], success=True,
                                   success_desc="ویدیو با موفیت آپلود شد")
        else:
            return render_template("add_video.html", form_all_tags=['سرگرمی', 'آموزشی'])

    @app.route('/videos/s/<video_id>', methods=['GET'])
    @must_be_user
    def get_stream_of_user(video_id):
        video = VideoService.get(video_id)
        if video is None:
            return json.dumps({"error": "file not found"})
        return render_template("show_video.html", video=video)

    @app.route('/tickets/new')
    def tickets():
        return render_template("new_ticket.html")

    @app.route('/api/tickets/new', methods=['POST'])
    @must_be_user
    def new_ticket():
        user_id = request.user._id
        ticket_message = request.form['ticket_message']
        TicketService.create_ticket(user_id=user_id, message=ticket_message)
        return json.dumps({'success': True})

    @app.route('/tickets/<ticket_id>', methods=['GET'])
    def show_ticket(ticket_id):
        ticket = TicketService.get_ticket_by_id(ticket_id)
        user = UserService.get_user_by_id(ticket.user)
        return render_template('ticket.html', ticket=ticket, user=user)