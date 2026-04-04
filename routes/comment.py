from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint
from flask import request

comment_bp = Blueprint('comment', __name__)









@comment_bp.route("/comment/<int:post_id>", methods=["POST"])
@jwt_required()
def comment(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    comment = Comment(
        content=data["content"],
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    return {"msg": "Comment added"}
