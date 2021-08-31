from flask import Blueprint, request, make_response, jsonify, abort
from api.models import CommunityTag, CommunityTagSchema
from flask_jwt_extended import jwt_required
import json

# ルーティング設定
communitytag_router = Blueprint("communitytag_router", __name__)


@communitytag_router.errorhandler(400)
def error_handler(err):
    res = jsonify({"error": {"message": err.description["message"]}, "code": err.code})
    return res, err.code


@communitytag_router.route("/communitytag", methods=["GET"])
@jwt_required(optional=True)
def getCommunityTagList():

    try:
        communitytag = CommunityTag.getCommunityTagList()
        communitytag_schema = CommunityTagSchema(many=True)
        communitytag_list = communitytag_schema.dump(communitytag)

    except ValueError:
        abort(400, {"message": "get failed"})

    return make_response(jsonify({"code": 200, "communitytag_tags": communitytag_list}))
