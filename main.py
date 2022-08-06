from flask import Flask

from config import MONGO_URL, SECRET_KEY, STAFF_IP
from controller import add_routes
from pymodm import connect
import git

from service.user import UserService

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['STAFF_IP'] = STAFF_IP

if __name__ == "__main__":
    connect(MONGO_URL)
    UserService.register_admin()
    add_routes(app)


    @app.route('/git_update', methods=['POST'])
    def git_update():
        repo = git.Repo('.')
        origin = repo.remotes.origin
        repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        origin.pull()
        return '', 200


    app.run(debug=True, host="0.0.0.0")
