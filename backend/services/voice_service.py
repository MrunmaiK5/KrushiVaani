# backend/services/voice_service.py
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import your actual functions from your ML folder
from ml_models.chatbot.speech_to_text import convert_audio_to_text_from_file
from ml_models.chatbot.text_to_speech import convert_text_to_audio_file

def process_audio_to_text(audio_file_path):
    return convert_audio_to_text_from_file(audio_file_path)

def process_text_to_audio(text_to_speak):
    return convert_text_to_audio_file(text_to_speak)