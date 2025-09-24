# ml_models/chatbot/text_to_speech.py
from gtts import gTTS
import os

def convert_text_to_audio_file(text_to_speak, lang='en', filename='response.mp3'):
    try:
        tts = gTTS(text=text_to_speak, lang=lang, slow=False)
        # Save the file in a temporary location
        filepath = os.path.join("instance", filename)
        tts.save(filepath)
        return filepath
    except Exception as e:
        print(f"Failed to generate speech: {e}")
        return None