from flask import Blueprint, request, make_response, jsonify, session, abort
from api.models import ExampleAnswerSchema, ExampleAnswer
import json

# ルーティング設定
example_answer_router = Blueprint("example_answer_router", __name__)


@example_answer_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@example_answer_router.route("/example", methods=["GET"])
def getExampleAnswerList():

    contents = request.args

    if contents.get("index_id") is not None and contents.get("index_id") != "":
        request_dict = {"index_id": contents.get("index_id")}
    else:
        abort(400, {"message": "index_id is required"})

    try:
        example_answers = ExampleAnswer.getExampleAnswerList(request_dict)
        example_answer_schema = ExampleAnswerSchema(many=True)
    except ValueError:
        abort(400, {"message": "value is invalid"})

    return make_response(
        jsonify({"code": 200, "examples": example_answer_schema.dump(example_answers)})
    )
