from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
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
jwt = JWTManager(app)

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

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    ip = request.remote_addr

    rate_key = f"rate_limit:login:{ip}"
    if not rate_limit(rate_key, limit=10):
       return jsonify({"msg" : "Too many login attempts"}), 429

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"msg": "Invalid username or password"}), 401


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    # Create user
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@app.route("/posts", methods= ["POST"])
@jwt_required()
def create_post():
   data = request.json
   current_user_id = get_jwt_identity()

   start = time.time()
   post = Post(content = data["content"], user_id = current_user_id)
   followers = db.session.query(Follow.follower_id).filter(Follow.followed_id == current_user_id).all()
   
   for follower in followers:
     r.lpush(f"feed:{follwer[0]}", post.id)
   db.session.add(post)
   db.session.commit()
   duration = time.time() - start

   if duration > 0.2:
       logger.warning("Slow DB query", extra = {"duration" : duration})
       r.delete(f"user_feed : {data['user_id']}")
       return jsonify({"message": "Post created"}), 201

   return jsonify({
        "message": "Post created successfully",
        "post_id": post.id,
        "followers_updated": len(followers)
    }), 201
@app.route("/feed", methods=["GET"])
@jwt_required()
def get_feed():
    current_user_id = get_jwt_identity() 
    
    page = request.args.get("page", 1, type=int)
    per_page = 20
    cache_key =f"user_feed:{current_user_id}:page: {page}"
    rate_key = f"rate_limit:feed:{user_id}"

    if not rate_limit(rate_key, limit=60):
       return jsonify({"msg" : "Too many requests"}), 429

    # Check redis first
    cached = r.get(cache_key)
    if cached:
        logger.info("Cache hit")
        return cached, 200
    
    logger.info("Cache miss")
    
    # Get users this user follows
    following = db.session.query(Follow.following_id).filter(Follow.follower_id==current_user_id).all()
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
    response = jsonify({
       "page" : page,
       "total_pages" : posts.pages,
       "posts" : results
    })
    r.setex(cache_key, 60, response.get_data())
    return response

@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    return jsonify({
        "cpu_percent": cpu,
        "memory_percent": memory
    })

def rate_limit(key, limit=100, window=60):

    current = r.get(key)

    if current and int(current) >= limit:
       return False

    pipe = r.pipeline()
    pipe.incr(key)
    if not current:
       pipe.expire(key, window)

    pipe.execute()
    return True



if __name__ == "__main__":
    app.run(debug=True)
