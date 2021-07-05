import const


class SystemConfig:

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = const.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = const.SECRET_KEY


Config = SystemConfig
