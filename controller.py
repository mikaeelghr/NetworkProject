from flask import request, Flask
from flask import render_template
from flask import redirect, url_for
import json

from service.token import must_be_user, must_be_admin
from service.user import UserService
from service.video import VideoService


def add_routes(app: Flask):
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template("index.html")

    @app.route('/user/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        UserService.login(username, password)

        return json.dumps({'success': True})

    @app.route('/user/register', methods=['POST'])
    @must_be_admin
    def register():
        print(request.user)
        username = request.form['username']
        password = request.form['password']

        UserService.register(username, password)

        return json.dumps({'success': True})

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
