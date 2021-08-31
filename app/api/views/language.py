from flask import Blueprint, request, make_response, jsonify, abort
from api.models import Language, LanguageSchema
from flask_jwt_extended import jwt_required
import json

# ルーティング設定
language_router = Blueprint("language_router", __name__)


@language_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@language_router.route("/language", methods=["GET"])
@jwt_required(optional=True)
def getLanguageList():

    try:
        language = Language.getLanguageList()
        language_schema = LanguageSchema(many=True)
        language_list = language_schema.dump(language)

    except ValueError:
        abort(400, {"message": "get failed"})

    return make_response(jsonify({"code": 200, "languages": language_list}))
