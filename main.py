from flask import Flask

import os

from controller import add_routes
from flask import request
from pymodm import connect
import git

from service.user import UserService

app = Flask(__name__)

config = __import__(os.environ.get('CONFIG_PATH') or 'config')
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['STAFF_IP'] = config.STAFF_IP
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

connect(config.MONGO_URL)
UserService.register_admin()
add_routes(app)


@app.route('/git_update', methods=['POST'])
def git_update():
    print(request.form)
    repo = git.Repo('.')
    origin = repo.remotes.origin
    origin.pull()
    return '', 200


if __name__ == "__main__":
    app.run(debug=True)
