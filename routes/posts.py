from flask import Blueprint, request, jsonify
from extensions import db

# Define the Blueprint
post_bp = Blueprint('posts', __name__)

# A simple route to test the feed
@post_bp.route('/posts', methods=['GET'])
def get_posts():
    return jsonify({"message": "Welcome to the scalable social feed!", "posts": []}), 200

# A route to create a post (placeholder logic)
@post_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    return jsonify({"message": "Post created successfully", "content": data.get('content')}), 201
