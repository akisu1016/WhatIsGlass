import re
from api.database import db, ma
from sqlalchemy import *
from .answer import Answer
import datetime


class Index(db.Model):
    __tablename__ = "indices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.String(50), nullable=False)
    questioner = db.Column(db.Integer, nullable=False)
    frequently_used_count = db.Column(db.Integer, nullable=False)
    language_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<Index %r>" % self.name

    def getIndexList(request_dict):

        sort = request_dict["sort"]
        language_id = request_dict["language_id"]
        include_no_answer = request_dict["include_no_answer"]
        keyword = request_dict["keyword"]

        sort_terms = "date"
        if sort == "1":
            sort_terms = "date"
        elif sort == "2":
            sort_terms = "frequently_used_count"
        # elif sort == "3":
        #     sort_terms = "frequently_used_count"

        index_list = null

        if include_no_answer == "true":
            index_list = (
                db.session.query(
                    Index.id,
                    Index.index,
                    Index.questioner,
                    Index.frequently_used_count,
                    Index.language_id,
                    Index.date,
                    Answer.definition.label("best_answer"),
                )
                .outerjoin(Answer, Index.id == Answer.index_id)
                .filter(
                    Index.index.contains(f"%{keyword}%"),
                    Index.language_id == language_id,
                )
                .order_by(asc(text(f"indices.{sort_terms}")))
                .all()
            )
        elif include_no_answer == "false":
            index_list = (
                db.session.query(
                    Index.id,
                    Index.index,
                    Index.questioner,
                    Index.frequently_used_count,
                    Index.language_id,
                    Index.date,
                    Answer.definition.label("best_answer"),
                )
                .join(Answer, Index.id == Answer.index_id)
                .filter(
                    Index.index.contains(f"%{keyword}%"),
                    Index.language_id == language_id,
                )
                .order_by(asc(text(f"indices.{sort_terms}")))
                .all()
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
            "user_id",
            "index_id",
            "definition",
            "origin",
            "note",
            "informative_count",
            "best_answer",
        )
