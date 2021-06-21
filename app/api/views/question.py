from flask import Blueprint, request, make_response, jsonify, session
from api.models import Index, IndexSchema, Answer, AnswerSchema
import json

# ルーティング設定
question_router = Blueprint("question_router", __name__)


@question_router.route("/question", methods=["GET"])
def getIndexList():

    contents = request.args

    request_dict = {
        "sort": contents.get("sort"),
        "language_id": contents.get("language_id"),
        "include_no_answer": contents.get("include_no_answer"),
        "keyword": contents.get("keyword"),
    }

    indices = Index.getIndexList(request_dict)
    index_schema = IndexSchema(many=True)

    return make_response(jsonify({"code": 200, "indices": index_schema.dump(indices)}))


@question_router.route("/question", methods=["POST"])
def registIndex():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    indexData = json.loads(jsonData)

    # TODO : JsonDataにquestionerのIDを追加する

    index = Index.registIndex(indexData)
    index_schema = IndexSchema(many=True)

    return make_response(jsonify({"code": 201, "index": index_schema.dump(index)}))
