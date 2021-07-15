import re
from api.database import db, ma
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import relationship
from sqlalchemy import *


class Language(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<languages %r>" % self.id

    def getLanguageList():

        language_list = db.session.query(Language).order_by(asc(Language.id)).all()

        if language_list is None:
            return []
        else:
            return language_list


class UserLanguage(db.Model):
    __tablename__ = "users_languages"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey("languages.id"), primary_key=True)

    def __repr__(self):
        return "<users_languages %r>" % self

    def getUserLanguageList(user):

        user_id = user["id"]

        user_language_list = (
            db.session.query(
                UserLanguage.user_id,
                UserLanguage.language_id,
                Language.language,
            )
            .join(
                Language,
                UserLanguage.language_id == Language.id,
            )
            .filter(
                UserLanguage.user_id == user_id,
            )
            .all()
        )

        if user_language_list is None:
            return []
        else:
            return user_language_list

    def registUserLanguage(user):

        user_id = user["id"]

        for language in user["languages"]:
            record = UserLanguage(user_id=user_id, language_id=language)
            db.session.add(record)

        db.session.flush()
        db.session.commit()

        response = (
            db.session.query(
                UserLanguage.user_id,
                UserLanguage.language_id,
                Language.language,
            )
            .join(
                Language,
                UserLanguage.language_id == Language.id,
            )
            .filter(
                UserLanguage.index_id == user_id,
            )
            .all()
        )

        if response is None:
            return []
        else:
            return response


class LanguageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Language
        load_instance = True
        fields = ("id", "language")


class UserLanguageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLanguage
        load_instance = True
        fields = ("user_id", "language_id", "language")
