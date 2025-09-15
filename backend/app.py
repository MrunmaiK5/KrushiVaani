# backend/app.py
import os
import sys

# This code adds the project's root folder (D:\KrushiVaani) to Python's path
# It is a robust way to fix the "ModuleNotFoundError: No module named 'backend'"
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, jsonify
from backend.config import Config
from backend.extensions import db, bcrypt, cors, migrate # <-- Import from extensions

def create_app(config_class=Config):
    """Application Factory Function"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)

    # Import models here AFTER extensions are initialized
    from backend.models.user_model import User

    # Register the Blueprints (our routes)
    from backend.routes.user_routes import user_bp
    from backend.routes.fertilizer_routes import fertilizer_bp
    from backend.routes.hybrid_routes import hybrid_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(fertilizer_bp, url_prefix='/fertilizer')
    app.register_blueprint(hybrid_bp, url_prefix='/hybrid')  # <-- Add this line

    # A simple test route
    @app.route('/')
    def index():
        return jsonify(message="The KrushiVaani server is running and ready for authentication!")

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

