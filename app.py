from flask import Flask
from config import Config
from extensions import db, jwt

from routes.auth import auth_bp
from routes.posts import post_bp
from routes.feed import feed_bp
from routes.follow import follow_bp
from routes.like import like_bp
from routes.comment import comment_bp
from routes.recommend import recommend_bp

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
# This is the important one for your error:
app.config['JWT_ALGORITHM'] = 'HS256' 

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(post_bp, url_prefix='/posts')
app.register_blueprint(feed_bp, url_prefix='/feed')
app.register_blueprint(follow_bp, url_prefix='/follow')
app.register_blueprint(like_bp, url_prefix='/like')
app.register_blueprint(comment_bp, url_prefix='/comments')
app.register_blueprint(recommend_bp, url_prefix='/recommend')

if __name__ == "__main__":
    app.run(debug=True)
