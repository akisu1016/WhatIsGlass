from api import const
from datetime import timedelta


class SystemConfig:

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = const.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = const.SECRET_KEY

    # JWT署名鍵
    JWT_SECRET_KEY = const.JWT_SECRET_KEY
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SAMESITE="None"
    JWT_COOKIE_SECURE = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=72)


Config = SystemConfig
