from re import S
import re
from werkzeug.wrappers import response
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
from sqlalchemy import *
from api.database import db, ma
from .user import User
import datetime
import json


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    index_id = db.Column(db.Integer, nullable=False)
    definition = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(300), nullable=False)
    note = db.Column(db.String(200), nullable=False)
    informative_count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<Answer %r>" % self.id

    def getAnswerList(request_index_id):

        # select * from users
        answer_list = (
            db.session.query(Answer)
            .filter(request_index_id["index_id"] == Answer.index_id)
            .all()
        )

        if answer_list is None:
            return []
        else:
            return answer_list

    def getUserAnswerList(request_dict):

        from .index import Index

        # リクエストから取得
        print(request_dict["sort"])
        sort = int(request_dict["sort"]) if request_dict["sort"] is not None else 1
        language_id = request_dict["language_id"]
        user_id = request_dict["user_id"]

        answer_limit = (
            int(request_dict["answer_limit"])
            if request_dict["answer_limit"] != ""
            else 300
            if int(request_dict["answer_limit"]) > 300
            else 100
        )

        if sort == 1:
            answer_list = (
                db.session.query(
                    Answer.id,
                    Answer.index_id,
                    Answer.definition,
                    Answer.origin,
                    Answer.note,
                    Answer.informative_count,
                    Answer.date,
                    User.username,
                )
                .filter(
                    Answer.index_id == Index.id,
                    User.id == user_id,
                    Index.language_id == language_id,
                )
                .distinct(Answer.id)
                .order_by(desc(text("answers.date")))
                .limit(answer_limit)
                .all()
            )
        else:
            answer_list = (
                db.session.query(
                    Answer.id,
                    Answer.index_id,
                    Answer.definition,
                    Answer.origin,
                    Answer.note,
                    Answer.informative_count,
                    Answer.date,
                    User.username,
                )
                .filter(
                    Answer.index_id == Index.id,
                    User.id == user_id,
                    Index.language_id == language_id,
                )
                .distinct(Answer.id)
                .order_by(text("answers.date"))
                .limit(answer_limit)
                .all()
            )

        if answer_list == null:
            return []
        else:
            return answer_list

    def registAnswer(answer):

        # answerの登録処理
        record = Answer(
            id=0,
            user_id=1,
            index_id=answer["index_id"],
            definition=answer["definition"],
            origin=answer["origin"],
            note=answer["note"],
            informative_count=0,
            date=datetime.datetime.now(),
        )

        # insert into answers(id, user_id, informative_count...) values(...)
        db.session.add(record)
        db.session.flush()
        db.session.commit()
        answers_query = db.session.execute(
            "SELECT * from answers WHERE id = last_insert_id();"
        )

        for get_answer_id in answers_query:
            return int(get_answer_id.id)

    def makeResponseAnswer(answer_id):

        # answersとexampleのresponseの結合処理

        answer_sql = "SELECT * FROM answers WHERE id = %d" % (answer_id)
        answer_query = db.session.execute(answer_sql)
        example_sql = "SELECT * FROM example_answer WHERE answer_id = %d" % (answer_id)
        example_query = db.session.execute(example_sql)

        answer_schema = AnswerSchema(many=True)

        answer_json = answer_schema.dumps(answer_query)
        answer_dict = json.loads(answer_json)
        example_json = answer_schema.dumps(example_query)
        example_dict = json.loads(example_json)

        answer_dict[0]["example"] = example_dict

        return answer_dict


class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        load_instance = True
        fields = (
            "id",
            "user_id",
            "index_id",
            "example_id",
            "definition",
            "origin",
            "note",
            "informative_count",
            "date",
            "example_sentence",
            "categorytags",
        )
