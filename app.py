from flask import Flask, request, jsonify
from flask_migrate import migrate
from config import Config
from extensions import db, make_celery, migrate
from models import User, Post, Follow
import redis
import logging
import time
import psutil
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
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
@jwt_required
def get_feed():
    current_user_id = get_jwt_identity 
    cached_key =f"user_feed:{current_user_id}"
    
    # Check redis first
    cached = r.get(cache_key)
    if cached:
        logger.info("Cache hit")
        return cached, 200
    
    logger.info("Cache miss")
    
    # Get users this user follows
    following = db.session.query(Follow.followed_id).filter_by(follower_id=current_user_id).all()
    following_ids = [f[0] for f in following]
    
    if not following_ids:
       return jsonify([])

    # Get postsfrom followed users
    posts =(
      Post.query
      .filter(Post.user_id.in_(following_ids))
      .order_by(Post.id.desc())
      .limit(20)
      .all()
    )
    
    results = [{"id": p.id, "content": p.content} for p in posts]
    r.setex(cache_key, 60, jsonify(results).get_data())
    return jsonify(results)

@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    return jsonify({
        "cpu_percent": cpu,
        "memory_percent": memory
    })




