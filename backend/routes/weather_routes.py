# backend/routes/weather_routes.py
from flask import Blueprint, jsonify
from backend.services.weather_service import get_weather_by_city

weather_bp = Blueprint('weather_bp', __name__)

@weather_bp.route('/<string:city>', methods=['GET'])
def get_weather(city: str):
    try:
        weather_data = get_weather_by_city(city)
        return jsonify(weather_data), 200
    except (ValueError, Exception) as e:
        return jsonify({"error": str(e)}), 400
    