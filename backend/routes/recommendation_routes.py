<<<<<<< HEAD
=======
# from flask import Blueprint, request, jsonify
# # Make sure to import the correct service functions
# from ..services import crop_service, fertilizer_service, weather_service
# # Remove imports for QueryHistory, db, json if not used here

# recommendation_bp = Blueprint('recommendation_bp', __name__, url_prefix='/recommend')

# @recommendation_bp.route('/crop-and-fertilizer', methods=['POST'])
# def recommend_both():
#     """Predicts the best crop, then recommends a fertilizer for that crop."""
#     try:
#         input_data = request.get_json()
#         if not input_data:
#             return jsonify({"error": "No data provided"}), 400

#         # --- THIS IS THE CRITICAL FIX ---
#         # Step 1: Get live weather data first
#         weather = weather_service.get_weather_data_for_model(input_data['location'])
#         # Step 2: Add weather data AND rainfall to the input_data dictionary
#         input_data.update(weather)
#         input_data['rainfall'] = 100.0  # Use a sensible default for rainfall
#         # --------------------------------

#         # Step 3: Now predict the best crop using the COMPLETE data
#         predicted_crop = crop_service.recommend_crop(input_data) # Use recommend_crop directly

#         # Step 4: Use the predicted crop to recommend a fertilizer
#         input_data['crop'] = predicted_crop # Use lowercase 'crop' key
#         fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)

#         final_response = {
#             "crop_prediction": predicted_crop,
#             "fertilizer_prediction": fertilizer_result
#         }
#         return jsonify(final_response), 200

#     except Exception as e:
#         # Log the full error for debugging
#         print(f"Error in /crop-and-fertilizer: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# @recommendation_bp.route('/fertilizer-only', methods=['POST'])
# def recommend_fertilizer_only():
#     """Recommends a fertilizer for a user-specified crop."""
#     try:
#         input_data = request.get_json()
#         if not input_data or not input_data.get('crop'):
#             return jsonify({"error": "No crop provided"}), 400

#         # Add placeholder if needed by fertilizer_service
#         # input_data['soil_moisture'] = 50 
#         fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)
        
#         # The frontend expects { "prediction": ... } for this route
#         return jsonify({"prediction": fertilizer_result}), 200

#     except Exception as e:
#         print(f"Error in /fertilizer-only: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

>>>>>>> c1a451279ad8528d78550fa2f59895c93599359a

# from flask import Blueprint, request, jsonify
# from ..services import crop_service, fertilizer_service, weather_service

# recommendation_bp = Blueprint('recommendation_bp', __name__, url_prefix='/recommend')

# @recommendation_bp.route('/crop-and-fertilizer', methods=['POST'])
# def recommend_both():
#     """Predicts the best crop, then recommends a fertilizer for that crop."""
#     try:
#         input_data = request.get_json()
#         if not input_data:
#             return jsonify({"error": "No data provided"}), 400

#         # Add weather data (with fallback defaults)
#         weather = weather_service.get_weather_data_for_model(input_data.get('location', 'Pune')) or {}
#         input_data.update({
#             "temperature": weather.get("temperature", 25.0),
#             "humidity": weather.get("humidity", 70.0),
#             "rainfall": weather.get("rainfall", 100.0)
#         })

#         predicted_crop = crop_service.recommend_crop(input_data)
#         input_data["crop"] = predicted_crop

#         fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)

#         return jsonify({
#             "crop_prediction": predicted_crop,
#             "fertilizer_prediction": fertilizer_result
#         }), 200

#     except Exception as e:
#         import traceback; traceback.print_exc()
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# @recommendation_bp.route('/fertilizer-only', methods=['POST'])
# def recommend_fertilizer_only():
#     """Recommends fertilizer for a given crop."""
#     try:
#         input_data = request.get_json()
#         if not input_data or not input_data.get('crop'):
#             return jsonify({"error": "Crop is required"}), 400

#         fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)
#         return jsonify({"prediction": fertilizer_result}), 200

#     except Exception as e:
#         import traceback; traceback.print_exc()
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



from flask import Blueprint, request, jsonify
from ..services.crop_service import recommend_crop
from ..services.fertilizer_service import recommend_fertilizer
from ..services.weather_service import get_weather_data_for_model # New Import

recommendation_bp = Blueprint('recommendation_bp', __name__)

@recommendation_bp.route('/crop', methods=['POST'])
def crop_recommend():
    data = request.get_json()
    try:
        # Fetch live weather based on location provided in the form
        location = data.get('location', 'Pune')
        weather = get_weather_data_for_model(location)
        
        # Merge live weather into the crop prediction data
        full_data = {**data, **weather}
        
        result = recommend_crop(full_data)
        return jsonify({"status": "success", "recommended_crop": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@recommendation_bp.route('/fertilizer', methods=['POST'])
def fertilizer_recommend():
    data = request.get_json()
    result = recommend_fertilizer(data)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@recommendation_bp.route('/both', methods=['POST'])
def get_both_recommendations():
    """
    Unified endpoint: Fetches live weather, predicts crop, 
    and calculates fertilizer gaps in one request.
    """
    data = request.get_json()
    try:
        # Step 1: Fetch Real-time Weather Data
        location = data.get('location', 'Pune')
        weather = get_weather_data_for_model(location)
        
        # Merge form data (N, P, K, ph, location) with API weather
        full_data = {**data, **weather}

        # Step 2: Predict Crop using all 7 features
        crop = recommend_crop(full_data)

        # Step 3: Get Fertilizer for that specific crop
        fert_data = {**full_data, 'crop': crop}
        fertilizer = recommend_fertilizer(fert_data)

        return jsonify({
            "status": "success",
            "crop_prediction": crop,
            "fertilizer_prediction": fertilizer,
            "weather_used": weather  # Sending back for frontend visibility
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500