from flask import Blueprint, request, make_response, jsonify, session, abort
from api.models import (
    FavoriteIndex,
    FavoriteIndexSchema,
    Index,
    IndexSchema,
    IndexCategoryTag,
    IndexCategorytagSchema,
)
from flask_jwt_extended import jwt_required, current_user
import json

# ルーティング設定
favorite_index_router = Blueprint("favorite_index_router", __name__)


@favorite_index_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@favorite_index_router.route("/favorite-question", methods=["GET"])
@jwt_required()
def getFavoriteIndexList():

    try:
        contents = request.args

        # リクエストの初期値
        request_dict = {
            "sort": 1,
            "index_limit": 100,
        }

        if contents.get("sort") is not None and contents.get("sort") != "":
            request_dict["sort"] = contents.get("sort")

        if (
            contents.get("index_limit") is not None
            and contents.get("index_limit") != ""
        ):
            request_dict["index_limit"] = contents.get("index_limit")

        if (
            contents.get("language_id") is not None
            and contents.get("language_id") != ""
        ):
            request_dict["language_id"] = contents.get("language_id")
        else:
            abort(400, {"message": "language_id is required"})

        if current_user is not None:
            request_dict["user_id"] = current_user.id
        else:
            abort(400, {"message": "Login required"})

        indices = Index.getFavotiteIndexList(request_dict)
        index_schema = IndexSchema(many=True)
        indices_list = index_schema.dump(indices)

    except ValueError:
        abort(400, {"message": "get failed"})

    return make_response(
        jsonify({"code": 200, "indices": merge_indices_categorytags(indices_list)})
    )


@favorite_index_router.route("/favorite-question", methods=["POST"])
@jwt_required()
def registFavoriteIndex():

    # jsonデータを取得する
    jsonData = json.dumps(request.json)
    indexData = json.loads(jsonData)

    if indexData is None or not "index_id" in indexData or indexData["index_id"] == "":
        abort(400, {"message": "parameter is a required"})

    if current_user is not None:
        indexData["user_id"] = current_user.id
    else:
        abort(400, {"message": "Login required"})

    try:
        favorite_index = FavoriteIndex.registFavoriteIndex(indexData)
        favorite_index_schema = FavoriteIndexSchema(many=True)
        favorite_index_list = favorite_index_schema.dump(favorite_index)

    except ValueError:
        abort(400, {"message": "post failed"})

    return make_response(jsonify({"code": 201, "index": favorite_index_list}))


@favorite_index_router.route("/favorite-question", methods=["DELETE"])
@jwt_required()
def deleteFavoriteIndex():

    try:
        contents = request.args

        # リクエストの初期値
        request_dict = {
            "index_id": "",
        }

        if contents.get("index_id") is not None and contents.get("index_id") != "":
            request_dict["index_id"] = contents.get("index_id")
        else:
            abort(400, {"message": "index_id is required"})

        if current_user is not None:
            request_dict["user_id"] = current_user.id
        else:
            abort(400, {"message": "Login required"})

        favorite_index = FavoriteIndex.deleteFavoriteIndex(request_dict)

    except ValueError:
        abort(400, {"message": "get failed"})

    if favorite_index:
        return make_response(jsonify({"code": 204}))
    else:
        return abort(400, {"message": "delete failed"})


##見出しのリストとカテゴリータグリストをマージする
def merge_indices_categorytags(indices_list):

    indices_categorytag_list = []
    categorytag_schema = IndexCategorytagSchema(many=True)

    for indices_dict in indices_list:
        categorytags = IndexCategoryTag.getCategoryTagList(indices_dict)
        categorytags_list = categorytag_schema.dump(categorytags)
        indices_dict["categorytags"] = []
        for categorytags_dict in categorytags_list:
            if indices_dict["id"] == categorytags_dict["index_id"]:
                indices_dict["categorytags"].append(
                    {
                        "id": categorytags_dict["category_tag_id"],
                        "category_tag_name": categorytags_dict["category_name"],
                    }
                )
        indices_categorytag_list.append(indices_dict)

    return indices_categorytag_list
