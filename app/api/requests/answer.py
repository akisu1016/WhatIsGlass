from sqlalchemy.sql.expression import true
from cerberus import Validator
from api.database import db, ma
import re
from datetime import datetime, date


class ValidateAnswer:
    def validateGetUserAnswerList(request_dict):

        languages_query = db.session.execute(
            "SELECT id from languages where id = %s;" % request_dict["language_id"]
        )
        language_id = 1
        for get_launguages_id in languages_query:
            language_id = get_launguages_id.id

        schema = {
            "sort": {
                "empty": True,
            },
            "language_id": {
                "allowed": [language_id],
                "required": True,
                "empty": False,
                "nullable": False,
                "coerce": int,
            },
            "answer_limit": {
                "empty": True,
            },
        }

        # バリデータを作成
        v = Validator(schema)

        return v.validate(request_dict)

    def validateGetAnswerList(request_dict):

        # 見出しバリデーション用のリスト
        index_query = db.session.execute(
            "SELECT id from indices where id = %s;" % request_dict["index_id"]
        )
        index_id = 0
        for get_index_id in index_query:
            index_id = get_index_id.id

        schema = {
            "index_id": {
                "allowed": [index_id],
                "required": True,
                "empty": False,
                "nullable": False,
                "coerce": int,
            },
        }

        # バリデータを作成
        v = Validator(schema)

        return v.validate(request_dict)

    def validateRegistAnswer(request_dict):

        index_query = db.session.execute(
            "SELECT id from indices where id = %s;" % request_dict["index_id"]
        )
        index_id = 0
        for get_index_id in index_query:
            index_id = get_index_id.id

        schema = {
            "index_id": {
                "allowed": [index_id],
                "required": True,
                "empty": False,
                "nullable": False,
                "coerce": int,
            },
            "definition": {
                "required": True,
                "empty": False,
                "nullable": False,
            },
            "origin": {
                "empty": True,
            },
            "example": {
                "empty": True,
            },
            "note": {
                "empty": True,
            },
        }

        if "category_tag_id" in request_dict:
            categorytag_query = db.session.execute(
                "SELECT id from categorytags where id = %s;"
                % request_dict["category_tag_id"]
            )
            categorytag_id = 0
            for get_categorytag_id in categorytag_query:
                categorytag_id = get_categorytag_id.id
                dict = {
                    "category_tag_id": {
                        "allowed": [categorytag_id],
                        "required": True,
                        "empty": False,
                        "nullable": False,
                        "coerce": int,
                    }
                }
                schema.append(dict)

        # バリデータを作成
        v = Validator(schema)

        return v.validate(request_dict)
