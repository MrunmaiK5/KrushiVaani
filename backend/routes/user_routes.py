from flask import Blueprint, request, jsonify
from ..models.user_model import User
from ..extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__, url_prefix='/auth')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password')
    if not all([username, email, password]):
        return jsonify({"error": "All fields are required"}), 400
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({"error": "User with this email or username already exists"}), 409
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # The identity is now correctly just the user's ID
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid email or password"}), 401

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity() # This now correctly gets the user ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "location": user.location
    }), 200

@user_bp.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    new_location = data.get('location')
    if not new_location:
        return jsonify({"error": "Location not provided"}), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.location = new_location
    db.session.commit()
    return jsonify({"message": f"Location updated successfully to {new_location}"}), 200

