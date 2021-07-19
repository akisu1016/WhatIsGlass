import re
import base64
import os
from .language import UserLanguage
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

        record = User(
            username=username,
            email=email,
            password=password,
        )

        db.session.add(record)
        db.session.flush()

        user = db.session.execute("SELECT * from users WHERE id = last_insert_id();")

        for get_user_id in user:
            user_id = get_user_id.id

        # ユーザー言語の登録
        for language in request_dict["languages"]:
            record = UserLanguage(user_id=user_id, language_id=int(language))
            db.session.add(record)

        db.session.flush()
        db.session.commit()

        response = db.session.execute(
            "SELECT * from users WHERE id = last_insert_id();"
        )

        if response is None:
            return []
        else:
            return response

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
            response = jsonify({"msg": "login successful"})
            set_access_cookies(response, access_token)

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
        email_valid = (
            db.session.query(User).filter(User.id != id, User.email == email).first()
        )

        if email_valid is not None:
            return abort(400, {"message": "email already exists"})

        # ユーザー情報のアップデート
        user.username = username if username != "" else user.username
        user.email = email if email != "" else user.email

        if request_dict["languages"] != "":
            # ユーザー言語のアップデート
            db.session.query(UserLanguage).filter(User.id == user.id).delete(
                synchronize_session="fetch"
            )

            for language in request_dict["languages"]:
                record = UserLanguage(user_id=id, language_id=language)
                db.session.add(record)

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
            "languages",
            "access_token",
        )
