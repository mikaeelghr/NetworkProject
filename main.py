from flask import Flask

from config import MONGO_URL, SECRET_KEY
from controller import add_routes
from pymodm import connect

from service.user import UserService

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == "__main__":
    connect(MONGO_URL)
    UserService.register_admin()
    add_routes(app)
    app.run(debug=True)
