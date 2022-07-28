from flask import Flask

from config import MONGO_URL, SECRET_KEY
from controller import add_routes
from pymodm import connect

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == "__main__":
    connect(MONGO_URL)
    add_routes(app)
    app.run(debug=True)
