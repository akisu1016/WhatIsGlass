from flask import Blueprint, request, make_response, jsonify, session
from api.models import Index, IndexSchema
import json

# ルーティング設定
question_router = Blueprint("question_router", __name__)


@question_router.route("/question", methods=["GET"])
def getIndexList():
    indices = Index.getIndexList()
    index_schema = IndexSchema(many=True)

    return make_response(jsonify({"code": 200, "indices": index_schema.dump(indices)}))


@question_router.route("/question", methods=["POST"])
def registIndex():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    indexData = json.loads(jsonData)

    # JsonDataにquestionerのIDを追加する

    index = Index.registIndex(indexData)
    index_schema = IndexSchema(many=True)

    return make_response(jsonify({"code": 201, "index": index_schema.dump(index)}))
