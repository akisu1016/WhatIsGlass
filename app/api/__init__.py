from flask import Flask, make_response, jsonify
from .views.user import user_router
from .views.question import question_router
from flask_cors import CORS
from api.database import db
import config


def create_app():

    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    # CORS対応
    CORS(app)

    # DB設定を読み込む
    app.config.from_object("config.Config")
    db.init_app(app)

    app.register_blueprint(user_router, url_prefix="/api")
    app.register_blueprint(question_router, url_prefix="/api")

    return app


app = create_app()
