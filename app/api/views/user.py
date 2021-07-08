from flask import Blueprint, request, make_response, jsonify, abort
from api.models import User, UserSchema
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt, current_user
from email_validator import validate_email, EmailNotValidError
from ..token import jwt, Redis
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


# jwtがの有効性を確認するコールバック関数
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = Redis.get(jti)
    return token_in_redis is not None


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

    ## emailのバリデーション
    try:
        valid = validate_email(userData["email"])
        userData["email"] = valid.email
    except EmailNotValidError as e:
        abort(400, {"message": "email is incorrect"})

    try:
        user = User.registUser(userData)
        user_schema = UserSchema(many=True)
    except ValueError:
        abort(400, {"message": ValueError})

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

    ## emailのバリデーション
    try:
        valid = validate_email(userData["email"])
        userData["email"] = valid.email
    except EmailNotValidError as e:
        abort(400, {"message": "email is incorrect"})

    try:
        loginuser = User.loginUser(userData)
        login_user_schema = UserSchema(many=True)
    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(
        jsonify(
            {
                "code": 201,
                "login_user": login_user_schema.dump([loginuser]),
            }
        )
    )


@user_router.route("/logout", methods=["POST"])
@jwt_required()
def postuUserLogout():
    response = jsonify({"code": 204, "meg": "Access token revoked"})
    unset_jwt_cookies(response)
    jti = get_jwt()["jti"]
    Redis.set(jti, "")
    return response


@user_router.route("user/edit", methods=["POST"])
@jwt_required()
def postUserEdit():

    jsonData = json.dumps(request.json)
    userData = json.loads(jsonData)

    if (
        userData is None
        or not "email" in userData
        and not "username" in userData
        or userData["email"] == ""
        and userData["username"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    userData["user_id"] = current_user.id
    userData["username"] = "" if not "username" in userData else userData["username"]
    userData["email"] = "" if not "email" in userData else userData["email"]

    ## emailのバリデーション
    try:
        valid = validate_email(userData["email"])
        userData["email"] = valid.email
    except EmailNotValidError as e:
        abort(400, {"message": "email is incorrect"})

    try:
        user = User.editUser(userData)
        user_schema = UserSchema(many=True)
        print(user)
    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(jsonify({"code": 201, "users": user_schema.dump([user])}))
