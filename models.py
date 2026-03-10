from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable = False)

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)



class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default = datetime.utcnow)

class Follow(db.Model):
    __tablename__ = "followers"

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.Index("idx_following_created", "following_id", "created_at"),
    )


class Like(db.Model):

    __tablename__ = "Likes"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        default = datetime.utcnow
    )

    __table_args__ = (db.UniqueConstraint(
        'user_id',
        'post_id',
        name = 'unique_like'),
    )

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(
        db.Integer,
        primary_key =True
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable = False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id'),
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

