
# backend/routes/disease_routes.py

import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.services.disease_service import predict_disease

disease_bp = Blueprint('disease_bp', __name__)

# Define a folder to store uploaded images temporarily
UPLOAD_FOLDER = 'backend/temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@disease_bp.route('/predict', methods=['POST'])
def predict_disease_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        try:
            # Save the file to a temporary location
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # --- Call the service with the file path ---
            result = predict_disease(file_path)
            # -------------------------------------------

            # Clean up the uploaded file
            os.remove(file_path)

            if "error" in result:
                return jsonify(result), 500 # Model loading or prediction error

            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400