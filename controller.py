from flask import request, Flask
from flask import render_template
from flask import redirect, url_for
import json

from service.token import must_be_user, must_be_admin, TokenService
from service.user import UserService
from service.video import VideoService
from service.ticket import TicketService


def add_routes(app: Flask):
    # @app.route('/')
    @app.route('/index')
    def index():
        return render_template("index.html")


    @app.route('/user/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        user = UserService.login(username, password)
        access_token = TokenService.generateToken(user)
        return json.dumps({'success': True, 'token': access_token})

    @app.route('/user/register', methods=['POST'])
    # @must_be_admin
    def register():
        username = request.form['username']
        password = request.form['password']

        user = UserService.register(username, password)
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

    @app.route('/')
    def tickets():
        return render_template("new_ticket.html")

    @app.route('/tickets/new_ticket', methods=['POST'])
    @must_be_user
    def new_ticket():
        username = request.user.username
        print("HI")
        ticket_message = request.form['ticket_message']
        TicketService.create_ticket(username=username, message=ticket_message)
        return json.dumps({'success': True})
