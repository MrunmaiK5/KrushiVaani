from flask import Blueprint, request, jsonify
from backend.models.user_model import User, QueryHistory
from backend.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import json

user_bp = Blueprint('user_bp', __name__, url_prefix='/auth')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password')
    if not all([username, email, password]):
        return jsonify({"error": "All fields are required"}), 400
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({"error": "User with this email or username already exists"}), 409
    
    # This now correctly uses the __init__ and set_password methods from your model
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    user = User.query.filter_by(email=email).first()

    # This now correctly uses the check_password method from your model
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid email or password"}), 401

@user_bp.route('/history', methods=['GET'])
@jwt_required()
def get_user_history():
    user_id = get_jwt_identity()
    try:
        history_records = QueryHistory.query.filter_by(user_id=user_id).order_by(QueryHistory.timestamp.desc()).all()
        history_list = [
            {
                "query_type": record.query_type,
                "input_data": json.loads(record.input_data),
                "result_data": json.loads(record.result_data),
                "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for record in history_records
        ]
        return jsonify(history_list), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
   
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    # Get the user's ID securely from the access token
    user_id = get_jwt_identity() 
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Return the user's details
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

    # Update the user's location in the database
    user.location = new_location
    db.session.commit()
    
    return jsonify({"message": f"Location updated successfully to {new_location}"}), 200