from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db

follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return jsonify({"error": "You cannot follow yourself"}), 400
    
    return jsonify({"message": f"You are now following user {user_id}"}), 200

@follow_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"You have unfollowed user {user_id}"}), 200
