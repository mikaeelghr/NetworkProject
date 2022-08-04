from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
import models


def authenticate_with_token(f, allowed_roles, *args, **kwargs):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return {
                   "message": "Authentication Token is missing!",
                   "data": None,
                   "error": "Unauthorized"
               }, 401
    try:
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
        return authenticate_with_token(f, ["USER"], *args, **kwargs)

    return decorated


def must_be_authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return authenticate_with_token(f, ["USER", "STAFF"], *args, **kwargs)

    return decorated


def must_be_staff(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return authenticate_with_token(f, ["STAFF"], *args, **kwargs)

    return decorated


def must_be_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return authenticate_with_token(f, ["ADMIN"], *args, **kwargs)

    return decorated


class TokenService:
    @staticmethod
    def generateToken(user):
        return jwt.encode(
            payload={
                "username": user.username,
                "role": user.role,
            }, key=current_app.config["SECRET_KEY"])
