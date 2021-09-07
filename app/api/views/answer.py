from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.operators import exists
from api.models import Answer, AnswerSchema, ExampleAnswer, AnswerInformative
from api.requests.answer import ValidateAnswer
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
    request_dict = dict(index_id=contents.get("index_id"))

    if ValidateAnswer.validateGetAnswerList(request_dict) is False:
        abort(400, {"message": "parameter is a required"})

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
    request_dict = dict(
        sort=contents.get("sort"),
        language_id=contents.get("language_id"),
        answer_limit=contents.get("answer_limit"),
    )

    print(type(request_dict))

    if ValidateAnswer.validateGetUserAnswerList(request_dict) is False:
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

    if ValidateAnswer.validateRegistAnswer(answerData) is False:
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
