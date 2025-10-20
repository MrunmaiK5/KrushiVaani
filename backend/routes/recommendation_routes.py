# backend/routes/recommendation_routes.py

from flask import Blueprint, request, jsonify
from backend.services.crop_service import predict_crop
from backend.services.fertilizer_service import recommend_fertilizer
from backend.models.user_model import QueryHistory
from backend.extensions import db
import json

recommendation_bp = Blueprint('recommendation_bp', __name__)

# Route 1: For combined crop and fertilizer recommendation
@recommendation_bp.route('/crop-and-fertilizer', methods=['POST'])
def recommend_all_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        crop_result = predict_crop(data)
        data["Crop"] = crop_result.get("predicted_crop")
        fertilizer_result = recommend_fertilizer(data)

        final_response = {
            "crop_prediction": crop_result,
            "fertilizer_recommendation": fertilizer_result
        }
        
        # --- Save to History ---
        # Note: We need to get user_id from a JWT token in a real scenario
        # history_entry = QueryHistory(...)
        # db.session.add(history_entry)
        # db.session.commit()
        
        return jsonify(final_response), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route 2: For fertilizer recommendation only
@recommendation_bp.route('/fertilizer-only', methods=['POST'])
def recommend_fertilizer_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        result = recommend_fertilizer(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500