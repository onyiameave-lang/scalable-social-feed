from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer,  db.ForeignKey("user.id"))

class Follow(db.Model):
    __tablename__ = "followers"

    folower_id = db.Column(
        db.Integer,
        db.ForeignKey("user_id", ondelete= "CASCADE"), 
        primary_key = True
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete= "CASCADE"),
        primary_key = True
    )

    created_at = db.Column(db.DateTime, default=db.func.now())

    __table_args__ = (
        db.Index("idx_following_created", "following_id", "created_at"), 
    )