# backend/routes/chatbot_routes.py

from flask import Blueprint, request, jsonify
from backend.services.chatbot_service import get_chatbot_response

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def handle_chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Get the response from our service
        bot_response = get_chatbot_response(user_message)
        return jsonify({"reply": bot_response}), 200
        
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500