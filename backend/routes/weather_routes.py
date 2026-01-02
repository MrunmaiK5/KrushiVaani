
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.weather_service import get_weather_by_city
from ..models.user_model import User

weather_bp = Blueprint('weather_bp', __name__, url_prefix='/weather')

@weather_bp.route('/alert', methods=['GET'])
@jwt_required() # Protects the route
def get_user_weather_alert():
    try:
        # Get the user ID directly from the JWT identity
        user_id = get_jwt_identity() 
        
        user = User.query.get(user_id) # Use the ID to find the user in the database
        
        # Check if the user exists
        if not user:
             return jsonify({"error": "User associated with token not found"}), 404

        # Use the user's saved location, or default to Pune if they haven't set one
        location = user.location if user.location else "Pune" 
        
        # Fetch weather data for the determined location
        weather_data = get_weather_by_city(location)
        return jsonify(weather_data), 200 # Return the weather data successfully
        
    except Exception as e:
        # Log the full error on the backend for debugging purposes
        print(f"Error in weather route: {e}") 
        return jsonify({"error": "An internal server error occurred while fetching weather"}), 500