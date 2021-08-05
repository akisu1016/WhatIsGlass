from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.operators import exists
from api.models import Answer, AnswerSchema, ExampleAnswer, AnswerInformative
from flask_jwt_extended import jwt_required, current_user
from ..token import jwt
import json

# ルーティング設定
answer_router = Blueprint("answer_router", __name__)


@answer_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@answer_router.errorhandler(401)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@answer_router.route("/answer", methods=["GET"])
@jwt_required(optional=True)
def getAnswerList():

    contents = request.args

    if contents.get("index_id") is not None and contents.get("index_id") != "":
        request_dict = {"index_id": contents.get("index_id")}
    else:
        abort(400, {"message": "index_id is required"})

    try:
        answers = Answer.getAnswerList(request_dict)
        answer_schema = AnswerSchema(many=True)
    except ValueError:
        print(ValueError)

    return make_response(jsonify({"code": 200, "answers": answer_schema.dump(answers)}))


@answer_router.route("/user/answer-list", methods=["GET"])
@jwt_required()
def getUserAnswerList():

    contents = request.args
    if contents is None:
        abort(400, {"message": "parameter is a required"})

    try:
        # リクエストの初期値
        request_dict = {
            "sort": 1,
            "answer_limit": 100,
        }

        if current_user is not None:
            request_dict["user_id"] = current_user.id
        else:
            abort(400, {"message": "Login required"})

        if contents.get("sort") is not None and contents.get("sort") != "":
            request_dict["sort"] = contents.get("sort")

        if (
            contents.get("answer_limit") is not None
            and contents.get("answer_limit") != ""
        ):
            request_dict["answer_limit"] = contents.get("answer_limit")

        if (
            contents.get("language_id") is not None
            and contents.get("language_id") != ""
        ):
            request_dict["language_id"] = contents.get("language_id")
        else:
            abort(400, {"message": "language_id is required"})

        answers = Answer.getUserAnswerList(request_dict)
        answer_schema = AnswerSchema(many=True)
    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(jsonify({"code": 200, "answers": answer_schema.dump(answers)}))


@answer_router.route("/answer", methods=["POST"])
@jwt_required()
def registAnswer():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    answerData = json.loads(jsonData)

    if (
        answerData is None
        or "index_id" not in answerData
        or "definition" not in answerData
        or answerData["index_id"] == ""
        or answerData["definition"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    try:
        answer_id = Answer.registAnswer(answerData)
        ExampleAnswer.registExampleAnswer(answerData["example"], answer_id)
        response_query = Answer.makeResponseAnswer(answer_id)

    except ValueError:
        abort(400, {"message": "value is invalid"})

    return make_response(jsonify({"code": 201, "answer": response_query}))


# 回答役に立つカウントアップAPI
@answer_router.route("/count-up-informative", methods=["POST"])
@jwt_required()
def countupInformative():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    answerData = json.loads(jsonData)

    if (
        answerData is None
        or not "answer_id" in answerData
        or answerData["answer_id"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    if current_user is not None:
        answerData["user_id"] = current_user.id
    else:
        abort(400, {"message": "Login required"})

    try:
        answer = AnswerInformative.countupInformative(answerData)
        if answer != False:
            answer_schema = AnswerSchema(many=True)
            answer_list = answer_schema.dump(answer)
        else:
            abort(400, {"message": "count failed"})
    except ValueError:
        abort(400, {"message": "count failed"})

    return make_response(jsonify({"code": 201, "answer": answer_list[0]}))


# 回答役に立つカウントダウンAPI
@answer_router.route("/count-down-informative", methods=["POST"])
@jwt_required()
def countdownInformative():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    answerData = json.loads(jsonData)

    if (
        answerData is None
        or not "answer_id" in answerData
        or answerData["answer_id"] == ""
    ):
        abort(400, {"message": "parameter is a required"})

    if current_user is not None:
        answerData["user_id"] = current_user.id
    else:
        abort(400, {"message": "Login required"})

    try:
        answer = AnswerInformative.countdownInformative(answerData)
        if answer != False:
            answer_schema = AnswerSchema(many=True)
            answer_list = answer_schema.dump(answer)
        else:
            abort(400, {"message": "count failed"})
    except ValueError:
        abort(400, {"message": "count failed"})

    return make_response(jsonify({"code": 201, "answer": answer_list[0]}))
