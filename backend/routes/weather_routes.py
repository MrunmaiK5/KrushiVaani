from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.weather_service import get_weather_by_city
from ..models.user_model import User

weather_bp = Blueprint('weather_bp', __name__, url_prefix='/weather')

@weather_bp.route('/alert', methods=['GET'])
@jwt_required()
def get_user_weather_alert():
    try:
        user_identity = get_jwt_identity()
        user = User.query.get(user_identity['id'])
        location = user.location if user and user.location else "Pune"
        weather_data = get_weather_by_city(location)
        return jsonify(weather_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500