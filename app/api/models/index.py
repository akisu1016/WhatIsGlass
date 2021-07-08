import re
from api.database import db, ma
from sqlalchemy import *
from .answer import Answer
from .user import User
import datetime
from sqlalchemy.dialects import mysql


class Index(db.Model):
    __tablename__ = "indices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.String(50), nullable=False)
    questioner = db.Column(db.Integer, nullable=False)
    frequently_used_count = db.Column(db.Integer, nullable=False)
    language_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<Index %r>" % self.id

    def getIndexList(request_dict):
        # リクエストから取得
        sort = int(request_dict["sort"]) if request_dict["sort"] is not None else 1
        language_id = request_dict["language_id"]
        include_no_answer = (
            int(request_dict["include_no_answer"])
            if request_dict["include_no_answer"] is not ""
            else 1
        )
        keyword = request_dict["keyword"]
        index_limit = (
            int(request_dict["index_limit"])
            if request_dict["index_limit"] is not ""
            else 300
            if int(request_dict["index_limit"]) > 300
            else 100
        )

        # sortの条件を指定

        sort_terms = (
            "indices.date"
            if sort == 1
            else "indices.frequently_used_count, indices.date"
            if sort == 2
            else "indices.date, answer_count"
            if sort == 3
            else "indices.date"
        )

        # 回答者数を取得するためのクエリ
        answer_count = (
            db.session.query(
                Index.id.label("index_id"),
                func.count(Answer.index_id).label("answer_count"),
            )
            .outerjoin(Answer, Index.id == Answer.index_id)
            .group_by(Index.id)
            .subquery("answer_count")
        )

        # ベストアンサーを一覧取得するためのクエリ
        max_informative = (
            db.session.query(
                Answer.index_id, func.max(Answer.informative_count).label("max_count")
            )
            .group_by(Answer.index_id)
            .subquery("max_informative")
        )

        best_answer = (
            db.session.query(
                Answer.index_id, func.any_value(Answer.definition).label("best_answer")
            )
            .join(
                max_informative,
                Answer.index_id == max_informative.c.index_id,
            )
            .filter(Answer.informative_count == max_informative.c.max_count)
            .group_by(Answer.index_id)
            .having(func.max(Answer.date))
            .subquery("best_answer")
        )

        index_list = (
            db.session.query(
                Index.id,
                Index.index,
                User.username,
                Index.frequently_used_count,
                Index.language_id,
                Index.date,
                answer_count.c.answer_count.label("answer_count"),
                best_answer.c.best_answer,
            )
            .outerjoin(best_answer, Index.id == best_answer.c.index_id)
            .filter(
                Index.index.contains(f"{keyword}"),
                Index.language_id == language_id,
                User.id == Index.questioner,
                Index.id == answer_count.c.index_id,
            )
            .distinct(Index.id)
            .order_by(desc(text(f"{sort_terms}")))
            .limit(index_limit)
            .all()
            if include_no_answer == 1
            else db.session.query(
                Index.id,
                Index.index,
                User.username,
                Index.frequently_used_count,
                Index.language_id,
                Index.date,
                answer_count.c.answer_count.label("answer_count"),
                best_answer.c.best_answer,
            )
            .join(best_answer, Index.id == best_answer.c.index_id)
            .filter(
                Index.index.contains(f"{keyword}"),
                Index.language_id == language_id,
                User.id == Index.questioner,
                Index.id == answer_count.c.index_id,
            )
            .distinct(Index.id)
            .order_by(desc(text(f"{sort_terms}")))
            .limit(index_limit)
            .all()
            if include_no_answer == 2
            else db.session.query(
                Index.id,
                Index.index,
                User.username,
                Index.frequently_used_count,
                Index.language_id,
                Index.date,
                answer_count.c.answer_count.label("answer_count"),
                best_answer.c.best_answer,
            )
            .outerjoin(best_answer, Index.id == best_answer.c.index_id)
            .filter(
                Index.index.contains(f"{keyword}"),
                Index.language_id == language_id,
                Index.id == answer_count.c.index_id,
                User.id == Index.questioner,
                answer_count.c.answer_count == 0,
            )
            .distinct(Index.id)
            .order_by(desc(text(f"{sort_terms}")))
            .limit(index_limit)
            .all()
            if include_no_answer == 3
            else null
        )

        if index_list == null:
            return []
        else:
            return index_list

    def registIndex(indices):
        record = Index(
            id=0,
            index=indices["index"],
            questioner=indices["questioner"],
            frequently_used_count=0,
            language_id=indices["language_id"],
            date=datetime.datetime.now(),
        )

        db.session.add(record)
        db.session.flush()
        db.session.commit()

        response = db.session.execute(
            "SELECT * from indices WHERE id = last_insert_id();"
        )

        return response


class IndexSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Index
        load_instance = True
        fields = (
            "id",
            "index",
            "questioner",
            "language_id",
            "frequently_used_count",
            "date",
            "username",
            "index_id",
            "definition",
            "origin",
            "note",
            "informative_count",
            "best_answer",
            "answer_count",
        )
