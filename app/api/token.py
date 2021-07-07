from flask_jwt_extended import JWTManager
from api.const import REDIS_HOST, REDIS_PORT
import redis

jwt = JWTManager()


def init_jwt(app):
    jwt.init_app(app)


def connect_redis():

    return redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
    )


Redis = connect_redis()
