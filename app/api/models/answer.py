import re
from api.database import db, ma
import datetime


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
        return "<Answer %r>" % self.name

    def getAnswerList():

        # select * from users
        answer_list = db.session.query(Answer).all()

        if answer_list == None:
            return []
        else:
            return answer_list


class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        load_instance = True
        fields = (
            "id",
            "user_id",
            "index_id",
            "definition",
            "origin",
            "note",
            "informative_count",
            "date",
        )
