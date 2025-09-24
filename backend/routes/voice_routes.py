# backend/routes/voice_routes.py
from flask import Blueprint, request, jsonify, send_file
from backend.services.voice_service import process_audio_to_text, process_text_to_audio
import os

voice_bp = Blueprint('voice_bp', __name__, url_prefix='/voice')

@voice_bp.route('/recognize', methods=['POST'])
def recognize_speech():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file part"}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file temporarily in the instance folder
    filepath = os.path.join("instance", "temp_upload.wav")
    file.save(filepath)

    recognized_text = process_audio_to_text(filepath)
    os.remove(filepath) # Clean up

    return jsonify({"text": recognized_text})


@voice_bp.route('/synthesize', methods=['POST'])
def synthesize_speech():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    audio_file_path = process_text_to_audio(text)
    if audio_file_path:
        # After sending, clean up the generated audio file
        try:
            return send_file(audio_file_path, as_attachment=True, download_name='response.mp3')
        finally:
            os.remove(audio_file_path)
    else:
        return jsonify({"error": "Failed to generate audio"}), 500