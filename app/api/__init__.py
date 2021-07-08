from flask import Flask, make_response, jsonify
from .views.user import user_router
from .views.question import question_router
from .views.answer import answer_router
from .views.example_answer import example_answer_router
from flask_cors import CORS
from api.database import db
from api.token import jwt
import redis


def create_app():

    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    # CORS対応
    CORS(app)

    app.config.from_object("config.Config")
    db.init_app(app)

    jwt.init_app(app)

    app.register_blueprint(user_router, url_prefix="/api")
    app.register_blueprint(question_router, url_prefix="/api")
    app.register_blueprint(answer_router, url_prefix="/api")
    app.register_blueprint(example_answer_router, url_prefix="/api")

    return app


app = create_app()
