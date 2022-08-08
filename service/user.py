from pymodm.errors import DoesNotExist
from pymongo.errors import DuplicateKeyError

from models import User
from bson import ObjectId


class UserService:
    @staticmethod
    def login(username, password):
        try:
            user = User.objects.get({'username': username, 'password': password})
            if not user.verified:
                return None
            return user
        except DoesNotExist:
            return None

    # TODO: encrypt password
    @staticmethod
    def register(username, password, firstname, lastname, role='USER', verified=True):
        return User.objects.create(username=username, password=password,
                                   firstname=firstname, lastname=lastname,
                                   role=role, verified=verified)

    @staticmethod
    def register_admin():
        try:
            return User.objects.create(username='manager', password='supreme_manager#2022', role="ADMIN")
        except DuplicateKeyError:
            pass

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get({"_id": ObjectId(user_id)})

    @staticmethod
    def get_admin_id():
        return User.objects.get({"username": "manager"})._id

    @staticmethod
    def get_unverified_staffs():
        return User.objects.raw({"verified": False})

    @staticmethod
    def verify_staff(user_id):
        user = UserService.get_user_by_id(user_id)
        user.verified = True
        user.save()

    @staticmethod
    def get_all_users():
        return User.objects.raw({"role": "USER"})

    @staticmethod
    def unblock_user(user_id):
        user = UserService.get_user_by_id(user_id)
        user.unblock()
        print(user.deleted_videos)
        user.save()