from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ai_service import recommend_users

recommend_bp = Blueprint("recommend", __name__)


@recommend_bp.route("/recommend", methods= ["GET"])
@jwt_required()
def recommend():
   user_id = get_jwt_identity()
   user = recommend_users(user_id)
   return jsonify({"recommended_users" : users})

