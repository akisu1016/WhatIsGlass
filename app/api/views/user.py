from flask import Blueprint, request, make_response, jsonify, abort
from werkzeug.wrappers import response
from api.models import (
    User,
    UserSchema,
    UserFirstLanguage,
    UserSecondLanguage,
    UserLanguageSchema,
    UserCommunityTag,
    UserCommunityTagSchema,
)
from flask_jwt_extended import (
    jwt_required,
    unset_jwt_cookies,
    get_jwt,
    current_user,
    set_access_cookies,
)
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
        or not "first_languages" in userData
        or not "second_languages" in userData
        or not "community_tags" in userData
        or userData["username"] == ""
        or userData["email"] == ""
        or userData["password"] == ""
        or userData["first_languages"] == ""
        or userData["second_languages"] == ""
        or userData["community_tags"] == ""
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
        user_schema = UserSchema()
        dumped_user = user_schema.dump(user)

        response = jsonify({"code": 201, "user": merge_user_list([dumped_user])})
        set_access_cookies(response, user["access_token"])
    except ValueError:
        abort(400, {"message": "sigunup failed"})

    return make_response(response)


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
        loginuser_list = login_user_schema.dump([loginuser])

        response = jsonify({"code": 201, "user": merge_user_list(loginuser_list)})
        set_access_cookies(response, loginuser["access_token"])
    except ValueError:
        abort(400, {"message": "login failed"})

    return make_response(response)


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

    userData["user_id"] = current_user.id
    userData["username"] = "" if not "username" in userData else userData["username"]
    userData["email"] = "" if not "email" in userData else userData["email"]
    userData["first_languages"] = (
        "" if not "first_languages" in userData else userData["first_languages"]
    )
    userData["second_languages"] = (
        "" if not "second_languages" in userData else userData["second_languages"]
    )
    userData["community_tags"] = (
        "" if not "community_tags" in userData else userData["community_tags"]
    )

    if (
        userData is None
        or not "email" in userData
        and not "username" in userData
        and not "first_languages" in userData
        and not "second_languages" in userData
        and not "community_tags" in userData
        or userData["email"] == ""
        and userData["username"] == ""
        and userData["first_languages"] == ""
        and userData["second_languages"] == ""
        and userData["community_tags"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    ## emailのバリデーション
    if userData["email"] != "":
        try:
            valid = validate_email(userData["email"])
            userData["email"] = valid.email
        except EmailNotValidError as e:
            abort(400, {"message": "email is incorrect"})

    try:
        user = User.editUser(userData)
    except ValueError:
        abort(400, {"message": "edit failed"})

    return make_response(jsonify({"code": 201, "user": merge_user_list([user])}))


@user_router.route("/whoami", methods=["GET"])
@jwt_required()
def getLoginUser():

    user = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }
    user["first_languages"] = []
    user["second_languages"] = []
    user["community_tags"] = []
    UserFirstLanguageList = UserFirstLanguage.getUserFisrtLanguageList(user)
    UserSecondLanguageList = UserSecondLanguage.getUserSecondLanguageList(user)
    UserCommunityTagList = UserCommunityTag.getCommunityTagList(user)
    for UserFirstLanguageDict in UserFirstLanguageList:
        user["first_languages"].append(
            {
                "id": UserFirstLanguageDict["language_id"],
                "language": UserFirstLanguageDict["language"],
            }
        )
    for UserSecondLanguageDict in UserSecondLanguageList:
        user["second_languages"].append(
            {
                "id": UserSecondLanguageDict["language_id"],
                "language": UserSecondLanguageDict["language"],
            }
        )
    for UserCommunityTagDict in UserCommunityTagList:
        user["community_tags"].append(
            {
                "id": UserCommunityTagDict["community_tag_id"],
                "community_tag_name": UserCommunityTagDict["community_tag_name"],
            }
        )
    return make_response(jsonify({"code": 201, "user": user}))


##ユーザーと言語,コミュニティをマージする
def merge_user_list(user_list):

    merge_user_list = []
    user_language_schema = UserLanguageSchema(many=True)
    user_community_tag_schema = UserCommunityTagSchema(many=True)

    for user_dict in user_list:
        first_languages = UserFirstLanguage.getUserFisrtLanguageList(user_dict)
        second_languages = UserSecondLanguage.getUserSecondLanguageList(user_dict)
        community_tags = UserCommunityTag.getCommunityTagList(user_dict)
        first_languages_list = user_language_schema.dump(first_languages)
        second_languages_list = user_language_schema.dump(second_languages)
        community_tag_list = user_community_tag_schema.dump(community_tags)
        user_dict["first_languages"] = []
        user_dict["second_languages"] = []
        user_dict["community_tags"] = []
        for first_languages_dict in first_languages_list:
            if user_dict["id"] == first_languages_dict["user_id"]:
                user_dict["first_languages"].append(
                    {
                        "id": first_languages_dict["language_id"],
                        "language": first_languages_dict["language"],
                    }
                )

        for second_languages_dict in second_languages_list:
            if user_dict["id"] == second_languages_dict["user_id"]:
                user_dict["second_languages"].append(
                    {
                        "id": second_languages_dict["language_id"],
                        "language": second_languages_dict["language"],
                    }
                )

        for community_tag_dict in community_tag_list:

            if user_dict["id"] == community_tag_dict["user_id"]:
                user_dict["community_tags"].append(
                    {
                        "id": community_tag_dict["community_tag_id"],
                        "community_tag_name": community_tag_dict["community_tag_name"],
                    }
                )
        merge_user_list.append(user_dict)

    return merge_user_list[0]
