# backend/routes/chatbot_routes.py

from flask import Blueprint, request, jsonify
from backend.services.chatbot_service import get_bot_prediction

chatbot_bp = Blueprint('chatbot_bp', __name__, url_prefix='/chatbot')

@chatbot_bp.route('/predict', methods=['POST'])
def predict():
    """
    Receives a user message and returns the bot's intelligent response.
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400
        
    user_message = data['message']
    
    try:
        bot_response = get_bot_prediction(user_message)
        return jsonify({"response": bot_response}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500