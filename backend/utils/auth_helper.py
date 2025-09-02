from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User
from database import db

def create_user(data):
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    if User.query.filter_by(email=email).first():
        return False, "User already exists"
    user = User(name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return True, "User created"

def authenticate_user(data):
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return False, "Invalid credentials"
    # in a production project, return a JWT; keep simple now:
    return True, f"user:{user.id}"
