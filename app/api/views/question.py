from flask import Blueprint, request, make_response, jsonify, session, abort
from api.models import User
from api.models import Index, IndexSchema
from flask_jwt_extended import jwt_required, current_user
from ..token import jwt
import json

# ルーティング設定
question_router = Blueprint("question_router", __name__)


@question_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@question_router.route("/question", methods=["GET"])
@jwt_required(optional=True)
def getIndexList():

    try:
        contents = request.args

        # リクエストの初期値
        request_dict = {
            "sort": 1,
            "include_no_answer": 1,
            "keyword": "",
            "index_limit": 100,
        }

        if contents.get("sort") is not None and contents.get("sort") != "":
            request_dict["sort"] = contents.get("sort")

        if (
            contents.get("include_no_answer") is not None
            and contents.get("include_no_answer") != ""
        ):
            request_dict["include_no_answer"] = contents.get("include_no_answer")

        if (
            contents.get("index_limit") is not None
            and contents.get("index_limit") != ""
        ):
            request_dict["index_limit"] = contents.get("index_limit")

        if (
            contents.get("language_id") is not None
            and contents.get("language_id") != ""
        ):
            request_dict["language_id"] = contents.get("language_id")
        else:
            abort(400, {"message": "language_id is required"})

        indices = Index.getIndexList(request_dict)
        index_schema = IndexSchema(many=True)
    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(jsonify({"code": 200, "indices": index_schema.dump(indices)}))


@question_router.route("/question", methods=["POST"])
@jwt_required()
def registIndex():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    indexData = json.loads(jsonData)

    if (
        indexData is None
        or not "index" in indexData
        or not "language_id" in indexData
        or indexData["index"] == ""
        or indexData["language_id"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    if current_user is not None:
        indexData["questioner"] = current_user.id
    else:
        abort(400, {"message": "Login required"})

    try:
        index = Index.registIndex(indexData)
        index_schema = IndexSchema(many=True)
    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(jsonify({"code": 201, "index": index_schema.dump(index)}))


@question_router.route("user/question-list", methods=["GET"])
@jwt_required()
def getUserIndexList():

    try:
        contents = request.args

        # リクエストの初期値
        request_dict = {
            "sort": 1,
            "include_no_answer": 1,
            "index_limit": 100,
        }

        if current_user is not None:
            request_dict["user_id"] = current_user.id
        else:
            abort(400, {"message": "Login required"})

        if contents.get("sort") is not None and contents.get("sort") != "":
            request_dict["sort"] = contents.get("sort")

        if (
            contents.get("include_no_answer") is not None
            and contents.get("include_no_answer") != ""
        ):
            request_dict["include_no_answer"] = contents.get("include_no_answer")

        if (
            contents.get("index_limit") is not None
            and contents.get("index_limit") != ""
        ):
            request_dict["index_limit"] = contents.get("index_limit")

        if (
            contents.get("language_id") is not None
            and contents.get("language_id") != ""
        ):
            request_dict["language_id"] = contents.get("language_id")
        else:
            abort(400, {"message": "language_id is required"})

        indices = Index.getUserIndexList(request_dict)
        index_schema = IndexSchema(many=True)
    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(jsonify({"code": 200, "indices": index_schema.dump(indices)}))
