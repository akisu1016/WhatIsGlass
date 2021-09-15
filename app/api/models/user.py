import re
import base64
import os
from .language import UserFirstLanguage, UserSecondLanguage
from .community_tag import UserCommunityTag
from flask import abort, jsonify
from sqlalchemy.sql.functions import user
from sqlalchemy.dialects import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import response
from flask_jwt_extended import create_access_token, set_access_cookies
from email_validator import validate_email, EmailNotValidError
from api.database import db, ma


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    icon = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return "<User %r>" % self.id

    def registUser(request_dict):

        username = request_dict["username"]
        email = request_dict["email"]
        password = generate_password_hash(request_dict["password"], method="sha256")

        # ユーザーが存在するか確認
        user = db.session.query(User).filter(User.email == email).first()

        if user is not None:
            return abort(400, {"message": "user is already registered"})

        new_user = User(
            username=username,
            email=email,
            password=password,
        )

        db.session.add(new_user)
        db.session.flush()

        user_id = new_user.id

        # ユーザー言語の登録
        for first_language in request_dict["first_languages"]:
            record = UserFirstLanguage(user_id=user_id, language_id=int(first_language))
            db.session.add(record)

        # ユーザー言語の登録
        for second_language in request_dict["second_languages"]:
            record = UserSecondLanguage(
                user_id=user_id, language_id=int(second_language)
            )
            db.session.add(record)

        # ユーザーコミュニティの登録
        for community_tag in request_dict["community_tags"]:
            record = UserCommunityTag(
                user_id=user_id, community_tag_id=int(community_tag)
            )
            db.session.add(record)

        db.session.flush()
        db.session.commit()

        return new_user

    def loginUser(request_dict):
        email = request_dict["email"]
        password = request_dict["password"]

        # ユーザーが存在するか確認
        user = db.session.query(User).filter(User.email == email).first()

        if user is None or not check_password_hash(user.password, password):
            return abort(
                400, {"message": "Please check your login details and try again."}
            )
        else:

            access_token = create_access_token(identity=user)
            login_user = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "access_token": access_token,
            }

            return login_user

    def editUser(request_dict):

        id = request_dict["user_id"]
        username = request_dict["username"]
        email = request_dict["email"]

        # ユーザーが存在するか確認
        user = db.session.query(User).filter(User.id == id).first()

        if user is None:
            return abort(400, {"message": "Invalid request"})

        # Emailの存在確認
        if email != "":
            email_valid = (
                db.session.query(User)
                .filter(User.id != id, User.email == email)
                .first()
            )

            if email_valid is not None:
                return abort(400, {"message": "email already exists"})

        # ユーザー情報のアップデート
        user.username = username if username != "" else user.username
        user.email = email if email != "" else user.email

        # ユーザー言語のアップデート
        if request_dict["first_languages"] != "":
            db.session.query(UserFirstLanguage).filter(User.id == user.id).delete(
                synchronize_session="fetch"
            )

            for first_anguage in request_dict["first_languages"]:
                record = UserFirstLanguage(user_id=id, language_id=first_anguage)
                db.session.add(record)

        if request_dict["second_languages"] != "":
            db.session.query(UserSecondLanguage).filter(User.id == user.id).delete(
                synchronize_session="fetch"
            )

            for second_language in request_dict["second_languages"]:
                record = UserSecondLanguage(user_id=id, language_id=second_language)
                print("aaaaaaaaaaaaa")
                db.session.add(record)

        if request_dict["community_tags"] != "":
            UserCommunityTag.editCommunityTag(request_dict)

        db.session.flush()
        db.session.commit()

        update_user = {"id": user.id, "username": user.username, "email": user.email}

        return update_user


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = (
            "id",
            "username",
            "email",
            "password",
            "icon",
            "first_languages",
            "second_languages",
            "access_token",
        )
