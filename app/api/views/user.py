from flask import Blueprint, request, make_response, jsonify, abort
from api.models import User, UserSchema
import json

# ルーティング設定
user_router = Blueprint("user_router", __name__)


@user_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@user_router.route("/signup", methods=["POST"])
def postUserSignup():

    # jsonデータを取得する
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
    # jsonデータを取得する
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
        jsonify({"code": 201, "login_user": login_user_schema.dump([loginuser])})
    )


@user_router.route("/users", methods=["GET"])
def getUserList():
    users = User.getUserList()
    user_schema = UserSchema(many=True)

    return make_response(jsonify({"code": 200, "users": user_schema.dump(users)}))
