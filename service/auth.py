from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
import models
from service.req import ReqService


class AuthService:
    @staticmethod
    def generateToken(user):
        return jwt.encode(
            payload={
                "username": user.username,
                "role": user.role,
            }, key=current_app.config["SECRET_KEY"])

    @staticmethod
    def authenticate(f, allowed_roles, *args, **kwargs):
        token = None
        if "TOKEN" in request.cookies:
            token = request.cookies["TOKEN"]
        if not token or token == "":
            if 'NONE' in allowed_roles:
                request.authenticated = False
                return f(*args, **kwargs)
            else:
                return {
                           "message": "Authentication Token is missing!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401
        try:
            request.is_staff = False
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            if data['role'] not in allowed_roles:
                abort(404)
            current_user = models.User.objects.get({"username": data["username"]})
            if current_user is None:
                return {
                           "message": "Invalid Authentication token!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401
            if current_user.blocked:
                abort(403)
            if current_user.role == "STAFF":
                if request.remote_addr == current_app.config["STAFF_IP"]:
                    request.is_staff = True
            request.authenticated = True
            request.user = current_user
            return f(*args, **kwargs)
        except Exception as e:
            return {
                       "message": "Something went wrong",
                       "data": None,
                       "error": str(e)
                   }, 500


def must_be_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return AuthService.authenticate(f, ["USER"], *args, **kwargs)

    return decorated


def must_be_authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return AuthService.authenticate(f, ["USER", "STAFF"], *args, **kwargs)

    return decorated


def must_be_supervisor(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return AuthService.authenticate(f, ["ADMIN", "STAFF"], *args, **kwargs)

    return decorated


def authenticate_if_token_exists(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return AuthService.authenticate(f, ["USER", "STAFF", "NONE"], *args, **kwargs)

    return decorated


def must_be_staff(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return AuthService.authenticate(f, ["STAFF"], *args, **kwargs)

    return decorated


def must_be_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return AuthService.authenticate(f, ["ADMIN"], *args, **kwargs)

    return decorated

def ddos_checker(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        thr = 1000
        host_addr = "127.0.0.1"
        if request.remote_addr == host_addr:
            return f(*args, **kwargs)
        ReqService.create_req(request.remote_addr)
        if ReqService.get_user_recent_reqs(request.remote_addr) > thr:
            return {"message": "too many requests",
                               "data": None,
                               "error": "DDoS"}, 403
        return f(*args, **kwargs)
    return decorated