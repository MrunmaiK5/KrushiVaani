import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import json

# Define paths relative to the current file's location
SCRIPT_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'ml_models', 'disease_detection', 'disease_cnn.h5')
MAPPING_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'ml_models', 'disease_detection', 'data', 'class_mapping.json')

# --- Load the model and class mapping once when the service starts ---
try:
    # Load the trained model
    model = load_model(MODEL_PATH)
    print("Disease detection model loaded successfully.")
    
    # Load the class name mapping
    with open(MAPPING_PATH, 'r') as f:
        class_mapping = json.load(f)
    print("Class mapping loaded successfully.")

except Exception as e:
    print(f"Error loading ML components: {e}")
    model = None
    class_mapping = None

# --- Define Advice for each disease ---
ADVICE = {
    "Pepper__bell___Bacterial_spot": "Apply copper fungicides and remove infected leaves. Ensure good air circulation.",
    "Pepper__bell___healthy": "Your pepper plant is healthy. Continue with regular watering and fertilizing.",
    "Potato___Early_blight": "Apply fungicides and ensure proper crop rotation. Remove and destroy affected leaves.",
    "Potato___Late_blight": "Use fungicides, practice good drainage, and ensure plants are well-spaced.",
    "Potato___healthy": "Your potato plant is healthy. Continue with regular care.",
    "Tomato_Bacterial_spot": "Use copper-based sprays and remove infected plant parts. Avoid overhead watering.",
    "Tomato_Early_blight": "Apply fungicides and practice crop rotation. Ensure good soil drainage.",
    "Tomato_Late_blight": "Use fungicides, prune lower branches, and avoid excess nitrogen.",
    "Tomato_Leaf_Mold": "Improve air circulation and reduce humidity. Apply fungicides if necessary.",
    "Tomato_Septoria_leaf_spot": "Use fungicides and remove affected leaves. Avoid wetting the foliage.",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Apply insecticidal soap or miticides. Use neem oil as a natural repellent.",
    "Tomato__Target_Spot": "Use fungicides and maintain good garden hygiene. Remove and destroy infected leaves.",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "This is a viral disease. Remove and destroy infected plants immediately to prevent spread. Control whitefly populations, which transmit the virus.",
    "Tomato__Tomato_mosaic_virus": "This is a viral disease. Remove and destroy infected plants. Sanitize tools to prevent spread.",
    "Tomato_healthy": "Your tomato plant is healthy. Continue with regular care."
}

def predict_disease(image_path):
    """
    Takes an image file path, preprocesses it, and predicts the disease.
    
    Args:
        image_path (str): The file path to the uploaded image.
        
    Returns:
        dict: A dictionary containing the prediction and corresponding advice.
    """
    if model is None or class_mapping is None:
        return {"error": "ML model not loaded. Please check the backend setup."}

    try:
        # Load and preprocess the image
        img = load_img(image_path, target_size=(128, 128))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Make the prediction
        predictions = model.predict(img_array)
        
        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Get the disease name from the class mapping
        disease_name = class_mapping.get(str(predicted_class_index), "Unknown")
        
        # Get the advice
        advice = ADVICE.get(disease_name, "No specific advice found for this case. Please consult a local expert.")

        return {
            "prediction": disease_name,
            "confidence": f"{np.max(predictions) * 100:.2f}%",
            "advice": advice
        }

    except Exception as e:
        return {"error": f"An error occurred during prediction: {e}"}

# --- For local testing (optional) ---
if __name__ == "__main__":
    sample_image_path = os.path.join(SCRIPT_DIR, '..', '..', 'ml_models', 'disease_detection', 'data', 'test', 'Tomato_Early_blight', '0a4b8686-2a6c-4820-994c-1d015c9247fe___RS_Early.B 7604.JPG')
    
    if os.path.exists(sample_image_path):
        result = predict_disease(sample_image_path)
        print("Prediction Result:")
        print(json.dumps(result, indent=4))
    else:
        print(f"Test image not found at: {sample_image_path}")
        print("Please provide a valid path to an image file for testing.")