from flask import Flask
from flask_cors import CORS
from .extensions import db, bcrypt, migrate, jwt
from .config import Config
from .models.user_model import User

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # THIS IS THE FINAL FIX: Use the new decorator to add claims
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = User.query.get(identity)
        if user:
            # This adds the username and email to the token payload
            return {"username": user.username, "email": user.email}
        return {}

    # Import and Register all your blueprints
    from .routes.user_routes import user_bp
    from .routes.recommendation_routes import recommendation_bp
    from .routes.weather_routes import weather_bp
    from .routes.chatbot_routes import chatbot_bp
    from .routes.voice_routes import voice_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(voice_bp)

    @app.route("/")
    def index():
        return {"message": "Welcome to the KrushiVaani Flask API!"}

    return app

