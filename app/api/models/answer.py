from api.database import db, ma
from sqlalchemy import create_engine, text
from .example import Example
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
        return "<Answer %r>" % self.definition

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

    def registAnswer(answer):

        record = Answer(
            id=0,
            user_id=1,
            informative_count=0,
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

        # exampleの登録処理(example.py作成時に記入予定)
        if not answer["example"]:
            return []
        else:
            for examplelist in answer["example"]:
                answer_query = db.session.execute(
                    "SELECT id from answers WHERE id = last_insert_id();"
                )

                sql = (
                    "INSERT INTO example_answer(example_sentence, answer_id) VALUES('%s', '%d)"
                    % (examplelist, answer_query[0][0])
                )
                db.session.execute(sql)

        return answer


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
