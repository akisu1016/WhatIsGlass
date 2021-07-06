from flask import Blueprint, request, make_response, jsonify, abort
from api.models import User, UserSchema
from flask_jwt_extended import (
    get_jwt_identity,
    current_user,
    jwt_required,
    unset_jwt_cookies,
    get_jwt,
    create_access_token,
    set_access_cookies,
)
from ..token import jwt
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import json

# ルーティング設定
user_router = Blueprint("user_router", __name__)


@user_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


# JWTの作成に使われた User オブジェクトをjsonにフォーマット
@jwt.user_identity_loader
def user_identity_lookup(user):

    return user.id


# 自動的にUserオブジェクトをロードするコールバック関数
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@user_router.route("/signup", methods=["POST"])
def postUserSignup():

    jsonData = json.dumps(request.json)
    userData = json.loads(jsonData)

    if (
        not "username" in userData
        or not "email" in userData
        or not "password" in userData
        or userData["username"] == ""
        or userData["email"] == ""
        or userData["password"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    try:
        user = User.registUser(userData)
        user_schema = UserSchema(many=True)
    except ValueError:
        print(ValueError)

    return make_response(jsonify({"code": 201, "users": user_schema.dump(user)}))


@user_router.route("/login", methods=["POST"])
def postUserLogin():

    jsonData = json.dumps(request.json)
    userData = json.loads(jsonData)

    if (
        not "email" in userData
        or not "password" in userData
        or userData["email"] == ""
        or userData["password"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    try:
        loginuser = User.loginUser(userData)
        login_user_schema = UserSchema(many=True)
    except ValueError:
        print(ValueError)

    return make_response(
        jsonify(
            {
                "code": 201,
                "login_user": login_user_schema.dump([loginuser]),
            }
        )
    )


@user_router.route("/logout", methods=["POST"])
def postuUserLogout():
    response = jsonify({"code": 204})
    unset_jwt_cookies(response)
    return response


@user_router.route("/protected", methods=["GET"])
@jwt_required(optional=True)
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@user_router.route("/who_am_i", methods=["GET"])
@jwt_required()
def whoami():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
    )
