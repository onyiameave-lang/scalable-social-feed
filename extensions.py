from flask_sqlalchemy import SQLAlchemy 
from redis import Redis 
from celery import Celery 

db = SQLAlchemy()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker = app.config["REDIS_URL"]
    )
    celery.conf.update(app.config)
    return celery