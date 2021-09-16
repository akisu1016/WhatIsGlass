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
    date = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<Answer %r>" % self.id

    def getAnswerList(request_index_id):

        informative_count = AnswerInformative.countInformative()

        # select * from users
        answer_list = (
            db.session.query(
                Answer.id,
                Answer.user_id,
                Answer.index_id,
                Answer.definition,
                Answer.origin,
                Answer.note,
                func.ifnull(informative_count.c.informative_count, 0).label(
                    "informative_count"
                ),
                Answer.date,
            )
            .outerjoin(
                informative_count,
                Answer.id == informative_count.c.answer_id,
            )
            .filter(request_index_id["index_id"] == Answer.index_id)
            .all()
        )

        if answer_list is None:
            return []
        else:
            return answer_list

    def getAnswer(answer_id):

        informative_count = AnswerInformative.countInformative()

        answer = (
            db.session.query(
                Answer.id,
                Answer.user_id,
                Answer.index_id,
                Answer.definition,
                Answer.origin,
                Answer.note,
                func.ifnull(informative_count.c.informative_count, 0).label(
                    "informative_count"
                ),
                Answer.date,
            )
            .outerjoin(
                informative_count,
                Answer.id == informative_count.c.answer_id,
            )
            .filter(
                Answer.id == answer_id,
            )
            .all()
        )

        if answer is None:
            return []
        else:
            return answer

    def getUserAnswerList(request_dict):

        from .index import Index

        # リクエストから取得
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

        informative_count = AnswerInformative.countInformative()

        answer_list = (
            db.session.query(
                Answer.id,
                Answer.user_id,
                Answer.index_id,
                Answer.definition,
                Answer.origin,
                Answer.note,
                func.ifnull(informative_count.c.informative_count, 0).label(
                    "informative_count"
                ),
                Answer.date,
                User.username,
            )
            .outerjoin(
                informative_count,
                Answer.id == informative_count.c.answer_id,
            )
            .filter(
                Answer.index_id == Index.id,
                User.id == user_id,
                Index.language_id == language_id,
            )
            .distinct(Answer.id)
        )

        if sort == 1:
            answer_list = answer_list.order_by(desc(text("answers.date")))
        else:
            answer_list = answer_list.order_by(text("answers.date"))

        answer_list = answer_list.limit(answer_limit)
        answer_list = answer_list.all()

        if answer_list == "":
            return []
        else:
            return answer_list

    def registAnswer(answer):

        # answerの登録処理
        record = Answer(
            user_id=1,
            index_id=answer["index_id"],
            definition=answer["definition"],
            origin=answer["origin"],
            note=answer["note"],
            date=datetime.datetime.now(),
        )

        # insert into answers(id, user_id, informative_count...) values(...)
        db.session.add(record)
        db.session.flush()
        db.session.commit()

        return record

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


class AnswerInformative(db.Model):
    __tablename__ = "answers_informative"

    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<answers_informative %r>" % self.answer_id, self.user_id

    def countupInformative(request):
        answer_id = request["answer_id"]
        user_id = request["user_id"]

        # 存在確認
        Informative_exist = (
            db.session.query(AnswerInformative)
            .filter(
                AnswerInformative.user_id == user_id,
                AnswerInformative.answer_id == answer_id,
            )
            .first()
        )

        if Informative_exist is not None:
            return False

        try:
            record = AnswerInformative(user_id=user_id, answer_id=answer_id)
            db.session.add(record)
            db.session.flush()
            db.session.commit()
        except ValueError:
            return False

        answer = Answer.getAnswer(answer_id)

        return answer

    def countdownInformative(request):
        answer_id = request["answer_id"]
        user_id = request["user_id"]

        # 存在確認
        Informative_exist = (
            db.session.query(AnswerInformative)
            .filter(
                AnswerInformative.user_id == user_id,
                AnswerInformative.answer_id == answer_id,
            )
            .first()
        )

        if Informative_exist is None:
            return False

        try:
            db.session.query(AnswerInformative).filter(
                AnswerInformative.answer_id == answer_id,
                AnswerInformative.user_id == user_id,
            ).delete(synchronize_session="fetch")
            db.session.flush()
            db.session.commit()
        except ValueError:
            return

        answer = Answer.getAnswer(answer_id)

        return answer

    def countInformative():

        informative_count = (
            db.session.query(
                AnswerInformative.answer_id,
                func.count(AnswerInformative.answer_id).label("informative_count"),
            )
            .group_by(AnswerInformative.answer_id)
            .subquery("informative_count")
        )

        return informative_count


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
