import os


class SystemConfig:

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4".format(
            **{
                "user": os.getenv("DB_USER", "glass"),
                "password": os.getenv("DB_PASSWORD", "glass"),
                "host": os.getenv("DB_HOST", "whatisglass_mysql"),
                "database": os.getenv("DB_DATABASE", "whatisglass"),
            }
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


Config = SystemConfig
