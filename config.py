import os 


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://myuser:mypassword@localhost:5432/scalable_social_feed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")