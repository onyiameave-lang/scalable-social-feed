from flask import Flask, request, jsonify
from config import Config
from extensions import db, make_celery
from models import User, Post
import redis
import logging
import time
import psutil

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
r = redis.Redis.from_url(app.config["REDIS_URL"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    duration = time.time() - request.start_time
    logger.info("Request", extra={
        "path": request.path,
        "duration_ms": round(duration * 1000, 2),
    })
    return response 

@app.route("/posts", methods= ["POST"])
def create_post():
   data = request.json

   start = time.time()
   post = Post(content = data["content"], user_id = data["user_id"])
   db.session.add(post)
   db.session.commit()
   duration = time.time() - start

   if duration > 0.2:
       logger.warning("Slow DB query", extra = {"duration" : duration})
       r.delete(f"user_feed : {data['user_id']}")
       return jsonify({"message": "Post created"}), 201

@app.route("/feed/<int:user_id>")
def get_feed(user_id):
    cached = r.get(f"user_feed: {user_id}")

    if cached:
        logger.info("Cache hit")
        return cached
    
    logger.info("Cache miss")
    
    posts = Post.query.filter_by(user_id =user_id).all()
    results = [{"id": p.id, "content": p.content} for p in posts]
    r.setex(f"user_feed: {user_id}", 60, jsonify(results).get_data())
    return jsonify(results)

@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    return jsonify({
        "cpu_percent": cpu,
        "memory_percent": memory
    })




