from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint
feed_bp = Blueprint('feed', __name__)




@feed_bp.route("/feed", methods=["GET"])
@jwt_required()
def feed():
    user_id = get_jwt_identity()

    cached = r.get(f"feed:{user_id}")
    if cached:
        return cached

    posts = (
        db.session.query(Post)
        .join(Follow, Follow.following_id == Post.user_id)
        .filter(Follow.follower_id == user_id)
        .order_by(Post.created_at.desc())
        .limit(20)
        .all()
    )

    result = [{"id": p.id, "content": p.content} for p in posts]

    r.setex(f"feed:{user_id}", 60, str(result))

    return jsonify(result)
