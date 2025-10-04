from flask import Blueprint, request, jsonify
from ..services import crop_service, fertilizer_service, weather_service

recommendation_bp = Blueprint('recommendation_bp', __name__, url_prefix='/recommend')

@recommendation_bp.route('/crop-and-fertilizer', methods=['POST'])
def recommend_both():
    try:
        input_data = request.get_json()
        weather = weather_service.get_weather_data_for_model(input_data['location'])
        input_data.update(weather)
        input_data['rainfall'] = 100.0
        predicted_crop = crop_service.recommend_crop(input_data)
        input_data['crop'] = predicted_crop
        fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)
        final_response = {
            "crop_prediction": predicted_crop,
            "fertilizer_prediction": fertilizer_result
        }
        return jsonify(final_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recommendation_bp.route('/fertilizer-only', methods=['POST'])
def recommend_fertilizer_only():
    try:
        input_data = request.get_json()
        if not input_data or not input_data.get('crop'):
            return jsonify({"error": "No crop provided"}), 400
        fertilizer_result = fertilizer_service.recommend_fertilizer(input_data)
        return jsonify({"prediction": fertilizer_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500