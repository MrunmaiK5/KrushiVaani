# backend/models/user_model.py
from backend.extensions import db # <-- CHANGE THIS LINE

class User(db.Model):
    """Represents a user in the database."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    
class QueryHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query_type = db.Column(db.String(50), nullable=False)  # e.g., 'hybrid', 'weather'
    input_data = db.Column(db.Text, nullable=False)        # Storing input as a JSON string
    result_data = db.Column(db.Text, nullable=False)       # Storing result as a JSON string
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('query_histories', lazy=True))

    def __repr__(self):
        return f"<QueryHistory {self.id} for User {self.user_id}>"