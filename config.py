import os 


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://myuser:mypassword@localhost:5432/social_feed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    JWT_SECRET_KEY = "super-secret-key"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
