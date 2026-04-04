from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis

db = SQLAlchemy()
jwt = JWTManager()

r = redis.Redis(host="localhost", port = 6379, decode_responses = True)

