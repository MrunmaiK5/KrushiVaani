# backend/routes/user_routes.py

from flask import Blueprint, request, jsonify
from backend.models.user_model import User
from backend.extensions import db, bcrypt

# A Blueprint is a way to organize a group of related routes.
user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing data"}), 400

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        # For now, we return a simple success message.
        # Later, we will return a JWT token for secure authentication.
        return jsonify({"message": "Login successful", "user": {"username": user.username, "email": user.email}}), 200

    return jsonify({"error": "Invalid credentials"}), 401