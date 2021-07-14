from flask import Blueprint, request, make_response, jsonify, abort
from api.models import CategoryTag, CategorytagSchema
from flask_jwt_extended import jwt_required

# ルーティング設定
categorytag_router = Blueprint("categorytag_router", __name__)


@categorytag_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@categorytag_router.route("/categorytag", methods=["GET"])
@jwt_required(optional=True)
def getCategoryTagList():

    try:
        categorytags = CategoryTag.getCategoryTagList()
        categorytag_schema = CategorytagSchema(many=True)
        categorytags_list = categorytag_schema.dump(categorytags)

    except ValueError:
        abort(400, {"message": ValueError})

    return make_response(jsonify({"code": 200, "category_tags": categorytags_list}))
