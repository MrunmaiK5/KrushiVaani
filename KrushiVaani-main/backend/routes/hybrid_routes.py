# backend/routes/hybrid_routes.py

from flask import Blueprint, request, jsonify
from backend.services.crop_service import predict_crop
from backend.services.fertilizer_service import recommend_fertilizer

hybrid_bp = Blueprint('hybrid_bp', __name__)


@hybrid_bp.route('/recommend_all', methods=['POST'])
def recommend_all_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Step 1: Predict crop
        crop_result = predict_crop(data)

        # Step 2: Add predicted crop to the data
        data["Crop"] = crop_result.get("predicted_crop")

        # Step 3: Get fertilizer recommendation
        fertilizer_result = recommend_fertilizer(data)

        # Step 4: Combine results
        final_response = {
            "crop_prediction": crop_result,
            "fertilizer_recommendation": fertilizer_result
        }
        return jsonify(final_response), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
