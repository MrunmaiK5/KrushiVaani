# # backend/routes/recommendation_routes.py

# from flask import Blueprint, request, jsonify
# from backend.services.crop_service import predict_crop
# from backend.services.fertilizer_service import recommend_fertilizer
# from backend.models.user_model import QueryHistory
# from backend.extensions import db
# import json

# recommendation_bp = Blueprint('recommendation_bp', __name__)

# # Route 1: For combined crop and fertilizer recommendation
# @recommendation_bp.route('/crop-and-fertilizer', methods=['POST'])
# def recommend_all_route():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No data provided"}), 400

#     try:
#         crop_result = predict_crop(data)
#         data["Crop"] = crop_result.get("predicted_crop")
#         fertilizer_result = recommend_fertilizer(data)

#         final_response = {
#             "crop_prediction": crop_result,
#             "fertilizer_recommendation": fertilizer_result
#         }
        
#         # --- Save to History ---
#         # Note: We need to get user_id from a JWT token in a real scenario
#         # history_entry = QueryHistory(...)
#         # db.session.add(history_entry)
#         # db.session.commit()
        
#         return jsonify(final_response), 200
#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# # Route 2: For fertilizer recommendation only
# @recommendation_bp.route('/fertilizer-only', methods=['POST'])
# def recommend_fertilizer_route():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No data provided"}), 400

#     try:
#         result = recommend_fertilizer(data)
#         return jsonify(result), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


from flask import Blueprint, request, jsonify
# Make sure to import the correct service functions
from ..services import crop_service, fertilizer_service, weather_service
# Remove imports for QueryHistory, db, json if not used here

recommendation_bp = Blueprint('recommendation_bp', __name__, url_prefix='/recommend')

@recommendation_bp.route('/crop-and-fertilizer', methods=['POST'])
def recommend_both():
    """Predicts the best crop, then recommends a fertilizer for that crop."""
    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "No data provided"}), 400

        # --- THIS IS THE CRITICAL FIX ---
        # Step 1: Get live weather data first
        weather = weather_service.get_weather_data_for_model(input_data['location'])
        # Step 2: Add weather data AND rainfall to the input_data dictionary
        input_data.update(weather)
        input_data['rainfall'] = 100.0  # Use a sensible default for rainfall
        # --------------------------------

        # Step 3: Now predict the best crop using the COMPLETE data
        predicted_crop = crop_service.recommend_crop(input_data) # Use recommend_crop directly

        # Step 4: Use the predicted crop to recommend a fertilizer
        input_data['crop'] = predicted_crop # Use lowercase 'crop' key
        fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)

        final_response = {
            "crop_prediction": predicted_crop,
            "fertilizer_prediction": fertilizer_result
        }
        return jsonify(final_response), 200

    except Exception as e:
        # Log the full error for debugging
        print(f"Error in /crop-and-fertilizer: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@recommendation_bp.route('/fertilizer-only', methods=['POST'])
def recommend_fertilizer_only():
    """Recommends a fertilizer for a user-specified crop."""
    try:
        input_data = request.get_json()
        if not input_data or not input_data.get('crop'):
            return jsonify({"error": "No crop provided"}), 400

        # Add placeholder if needed by fertilizer_service
        # input_data['soil_moisture'] = 50 
        fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)
        
        # The frontend expects { "prediction": ... } for this route
        return jsonify({"prediction": fertilizer_result}), 200

    except Exception as e:
        print(f"Error in /fertilizer-only: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
