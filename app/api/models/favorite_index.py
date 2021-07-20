import re
from flask import abort
from sqlalchemy.sql.functions import user
from api.database import db, ma


class FavoriteIndex(db.Model):
    __tablename__ = "favorite_indices"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    index_id = db.Column(db.Integer, db.ForeignKey("indices.id"), primary_key=True)

    def __repr__(self):
        return "<favorite_indices %r>" % self

    def registFavoriteIndex(reqest):

        user_id = reqest["user_id"]
        index_id = reqest["index_id"]

        # お気に入りの存在確認
        favorite_valid = (
            db.session.query(FavoriteIndex)
            .filter(
                FavoriteIndex.user_id == user_id, FavoriteIndex.index_id == index_id
            )
            .first()
        )

        if favorite_valid is not None:
            return abort(400, {"message": "favorite index already exists"})

        record = FavoriteIndex(user_id=user_id, index_id=index_id)
        db.session.add(record)

        db.session.flush()
        db.session.commit()

        response = (
            db.session.query(FavoriteIndex.index_id)
            .filter(
                FavoriteIndex.index_id == index_id,
                FavoriteIndex.user_id == user_id,
            )
            .all()
        )

        if response is None:
            return []
        else:
            return response

    def deleteFavoriteIndex(reqest):

        user_id = reqest["user_id"]
        index_id = reqest["index_id"]

        try:
            db.session.query(FavoriteIndex).filter(
                FavoriteIndex.index_id == index_id, FavoriteIndex.user_id == user_id
            ).delete(synchronize_session="fetch")

            db.session.flush()
            db.session.commit()
        except ValueError:
            return False

        return True


class FavoriteIndexSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteIndex
        load_instance = True
        fields = ("user_id", "index_id")
