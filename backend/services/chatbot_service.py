# backend/services/chatbot_service.py

import sys
import os

# This adds the project's root directory to the Python path
# so we can import files from the ml_models folder.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# import actual prediction function
from ml_models.chatbot.final_predict import get_chatbot_response

def get_bot_prediction(user_message: str) -> str:
    """
    This is the real service function that calls the ML model.
    """
    if not user_message:
        return "I'm sorry, I didn't receive a message."
    
    response = get_chatbot_response(user_message)
    return response