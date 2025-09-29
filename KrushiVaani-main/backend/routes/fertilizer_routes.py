# backend/routes/fertilizer_routes.py

from flask import Blueprint, request, jsonify
from backend.services.fertilizer_service import recommend_fertilizer as service_recommend_fertilizer

fertilizer_bp = Blueprint('fertilizer_bp', __name__)

@fertilizer_bp.route('/recommend', methods=['POST'])
def recommend_fertilizer_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        result = service_recommend_fertilizer(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500