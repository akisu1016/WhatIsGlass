from flask import Blueprint, request, make_response, jsonify, abort
from api.models import (
    CategoryTag,
    CategorytagSchema,
    IndexCategoryTag,
    IndexCategorytagSchema,
    Index,
)
from flask_jwt_extended import jwt_required
import json

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
        abort(400, {"message": "get failed"})

    return make_response(jsonify({"code": 200, "category_tags": categorytags_list}))


@categorytag_router.route("/categorytag/edit", methods=["POST"])
@jwt_required()
def postCategoryTagList():

    jsonData = json.dumps(request.json)
    categorytagData = json.loads(jsonData)

    categorytagData["index_id"] = (
        "" if not "index_id" in categorytagData else categorytagData["index_id"]
    )

    categorytagData["category_tag_id"] = (
        ""
        if not "category_tag_id" in categorytagData
        else categorytagData["category_tag_id"]
    )

    if (
        categorytagData is None
        or not "index_id" in categorytagData
        or not "category_tag_id" in categorytagData
        or categorytagData["index_id"] == ""
        or categorytagData["category_tag_id"] == ""
        or len(categorytagData["category_tag_id"]) == 0
    ):
        abort(400, {"message": "parameter is a required"})

    try:

        Index_list = Index.getIndex(categorytagData["index_id"])

        if len(Index_list) == 0:
            abort(400, {"message": "index does not exist"})

        categorytags = IndexCategoryTag.editCategoryTag(categorytagData)
        categorytag_schema = CategorytagSchema(many=True)
        categorytags_list = categorytag_schema.dump(categorytags)

    except ValueError:
        abort(400, {"message": "post failed"})

    return make_response(
        jsonify(
            {
                "code": 200,
                "index_id": categorytagData["index_id"],
                "Category_tag": categorytags_list,
            }
        )
    )
