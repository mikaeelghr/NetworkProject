from flask import request, Flask
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

    @app.route('/api/user/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        user = UserService.login(username, password)
        if user is None:
            return json.dumps({'success': False})
        access_token = TokenService.generateToken(user)
        return json.dumps({'success': True, 'token': access_token})

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
        return json.dumps({'success': True, 'token': access_token})

    # code random, bayad avaz she
    @app.route('/videos/upload', methods=['GET', 'POST'])
    @must_be_user
    def upload_video():
        if request.method == 'POST':
            username = request.user.username
            if 'file' not in request.files or request.files['file'] == '':
                return redirect(request.url)
            file = request.files['file']
            VideoService.add(username, file)
            return redirect(url_for('videos/user/', username=username))

    @app.route('/videos/user/<username>', methods=['GET'])
    def get_stream_of_user(username):
        pass

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
