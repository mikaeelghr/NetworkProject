from pymongo.errors import DuplicateKeyError

from models import User


class UserService:
    @staticmethod
    def login(username, password):
        user = User.objects.get({'username': username, 'password': password})
        return user if user is not None else False

    # TODO: encrypt password
    @staticmethod
    def register(username, password):
        return User.objects.create(username=username, password=password, role="USER")

    @staticmethod
    def register_admin():
        try:
            return User.objects.create(username='admin', password='admin', role="ADMIN")
        except DuplicateKeyError:
            pass
