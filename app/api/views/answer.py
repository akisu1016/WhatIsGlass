from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy.sql.expression import true
from api.models import Answer, AnswerSchema, ExampleAnswer, ExampleAnswerSchema
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


@answer_router.route("/answer", methods=["POST"])
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
        answer = Answer.registAnswer(answerData)
        example = ExampleAnswer.registExampleAnswer(answerData)
        example_answer_schema = ExampleAnswerSchema(many=True)
        answer_schema = AnswerSchema(many=True)

    except ValueError:
        abort(400, {"message": "value is invalid"})

    return make_response(
        jsonify(
            {"code": 201, "answer": answer_schema.dump(answer)},
            {"code": 201, "example": example_answer_schema.dump(example)},
        )
    )
