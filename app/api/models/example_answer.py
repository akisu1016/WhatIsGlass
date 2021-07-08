import re
from api.database import db, ma
from .answer import Answer
import datetime


class ExampleAnswer(db.Model):
    __tablename__ = "example_answer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    example_sentence = db.Column(db.String(200), nullable=False)
    answer_id = db.Column(db.Integer, nullable=False)
    last_answer_id = 0

    def __repr__(self):
        return "<Answer %r>" % self.name

    def getExampleAnswerList(request_dict):

        index_id = request_dict["index_id"]

        example_answer_list = (
            db.session.query(
                ExampleAnswer.id,
                ExampleAnswer.example_sentence,
                ExampleAnswer.answer_id,
                Answer.index_id,
            )
            .join(Answer, ExampleAnswer.answer_id == Answer.id)
            .filter(
                Answer.index_id == index_id,
            )
            .all()
        )

        if example_answer_list is None:
            return []
        else:
            return example_answer_list

    def registExampleAnswer(answer):

        answers_query = db.session.execute(
            "SELECT * from answers WHERE id = last_insert_id();"
        )

        for get_answer_id in answers_query:
            ExampleAnswer.last_answer_id = int(get_answer_id.id)

        # exampleの登録処理

        if not answer["example"]:
            return answer
        else:
            for examplelist in answer["example"]:

                record = ExampleAnswer(
                    example_sentence=examplelist,
                    answer_id=ExampleAnswer.last_answer_id,
                )

                db.session.add(record)
                db.session.flush()

        db.session.commit()

        response = db.session.execute(
            "SELECT * from example_answer WHERE id = last_insert_id();"
        )

        return response


class ExampleAnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExampleAnswer
        load_instance = True
        fields = (
            "id",
            "example_sentence",
            "answer_id",
            "index_id",
        )
