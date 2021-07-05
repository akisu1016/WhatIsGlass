import re
import base64
import os
import secrets
from flask import abort
from sqlalchemy.sql.functions import user
from sqlalchemy.dialects import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import response
from api.database import db, ma

##一応saltも作っておく
salt = base64.b64encode(os.urandom(32))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    icon = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return "<User %r>" % self.name

    def getUserList():

        # select * from users
        user_list = db.session.query(User).all()

        if user_list == None:
            return []
        else:
            return user_list

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
        db.session.commit()

        response = db.session.execute(
            "SELECT * from users WHERE id = last_insert_id();"
        )

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
            login_user = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": secrets.token_hex(),
            }

            print(login_user)

            return login_user


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "username", "email", "password", "icon", "token")
