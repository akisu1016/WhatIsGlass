from api.database import db, ma
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

    def getIndexList():

        index_list = db.session.query(Index).all()

        if index_list == None:
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
        )
