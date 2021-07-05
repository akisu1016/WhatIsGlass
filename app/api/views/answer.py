from flask import Blueprint, request, make_response, jsonify, abort
from api.models import Answer, AnswerSchema
import json

# ルーティング設定
answer_router = Blueprint("answer_router", __name__)


@answer_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@answer_router.route("/answer", methods=["GET"])
def getAnswerList():

    print("aaaaaaaaa")
    try:
        contents = request.args
        request_dict = {
            "index_id": contents.get("index_id"),
        }
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

    if "answerer" not in answerData:
        abort(401, {"message": "answerer is a required!!"})
    elif "index_id" not in answerData:
        abort(400, {"message": "index is not exit"})

    try:
        answer = Answer.registAnswer(answerData)
        answer_schema = AnswerSchema(many=True)
    except ValueError:
        print(ValueError)

    return make_response(jsonify({"code": 201, "answer": answer_schema.dump(answer)}))
