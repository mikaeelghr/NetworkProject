from pymodm.errors import DoesNotExist
from pymongo.errors import DuplicateKeyError

from models import User
from bson import ObjectId


class UserService:
    @staticmethod
    def login(username, password):
        try:
            return User.objects.get({'username': username, 'password': password})
        except DoesNotExist:
            return None

    # TODO: encrypt password
    @staticmethod
    def register(username, password, firstname, lastname):
        return User.objects.create(username=username, password=password,
                                   firstname=firstname, lastname=lastname,
                                   role="USER")

    @staticmethod
    def register_admin():
        try:
            return User.objects.create(username='admin', password='admin', role="ADMIN")
        except DuplicateKeyError:
            pass

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get({"_id": ObjectId(user_id)})

    @staticmethod
    def get_admin_id():
        return User.objects.get({"username": "admin"})._id
