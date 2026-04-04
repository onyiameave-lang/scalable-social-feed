from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import Blueprint
like_bp = Blueprint('likes', __name__)




@like_bp.route("/like/<int:post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()

    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    return {"msg": "Post liked"}
