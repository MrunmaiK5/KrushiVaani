# backend/services/fertilizer_service.py
import os
import joblib
import numpy as np

# Resolve model path relative to project root (works when uvicorn is run from project root)
def find_model():
    candidates = [
        os.path.join(os.getcwd(), "ml-models", "fertilizer", "fertilizer_model.pkl"),
        os.path.join(os.getcwd(), "ml_models", "fertilizer", "fertilizer_model.pkl"),
        os.path.join(os.getcwd(), "ml-models", "fertilizer.pkl"),
        os.path.join(os.path.dirname(__file__), "..", "ml-models", "fertilizer", "fertilizer_model.pkl"),
        "/mnt/data/fertilizer_model.pkl"
    ]
    for p in candidates:
        p = os.path.abspath(p)
        if os.path.exists(p):
            return p
    return None

def find_features():
    candidates = [
        os.path.join(os.getcwd(), "ml-models", "fertilizer", "feature_names.pkl"),
        os.path.join(os.getcwd(), "ml_models", "fertilizer", "feature_names.pkl"),
        os.path.join(os.path.dirname(__file__), "..", "ml-models", "fertilizer", "feature_names.pkl"),
    ]
    for p in candidates:
        p = os.path.abspath(p)
        if os.path.exists(p):
            return p
    return None

MODEL_PATH = find_model()
FEATURES_PATH = find_features()

if MODEL_PATH:
    model = joblib.load(MODEL_PATH)
else:
    model = None

if FEATURES_PATH:
    features = joblib.load(FEATURES_PATH)
else:
    features = ["N","P","K","pH","soil_moisture"]  # fallback

# mapping crop -> fertilizer recommendations (fill/adjust as needed)
fertilizer_dict = {
    "rice": ["Urea", "DAP"],
    "maize": ["Urea", "MOP"],
    "chickpea": ["DAP", "Potash"],
    "kidneybeans": ["Urea", "FYM"],
    "pigeonpeas": ["DAP", "FYM"],
    "mothbeans": ["DAP", "FYM"],
    "mungbean": ["DAP", "FYM"],
    "blackgram": ["DAP", "FYM"],
    "lentil": ["DAP", "Potash"],
    "pomegranate": ["Potash", "Compost"],
    "banana": ["Urea", "Compost"],
    "mango": ["Compost", "Potash"],
    "grapes": ["Superphosphate", "Potash"],
    "watermelon": ["Urea", "MOP"],
    "muskmelon": ["Urea", "MOP"],
    "apple": ["Potash", "Compost"],
    "orange": ["Potash", "Compost"],
    "papaya": ["Balanced NPK", "Compost"],
    "coconut": ["Potash", "Compost"],
    "cotton": ["Urea", "Potash"],
    "jute": ["Balanced NPK"],
    "coffee": ["Compost", "Ammonium Sulphate"]
}

def recommend_fertilizer(input_data: dict):
    """Return ML crop prediction (if model present) + rule-based fertilizer list."""
    # Validate input has necessary fields:
    for f in features:
        if f not in input_data:
            raise ValueError(f"Missing required field: {f}")

    # Prepare feature vector
    values = [input_data[f] for f in features]
    values = np.array(values).reshape(1, -1)

    result = {}

    if model is not None:
        pred_crop = model.predict(values)[0]
        result["predicted_crop"] = str(pred_crop)
    else:
        result["predicted_crop"] = None

    # Get fertilizer recommendations (based on predicted crop if available)
    crop_key = result["predicted_crop"] or input_data.get("Crop")
    fertilizers = fertilizer_dict.get(str(crop_key).lower(), ["General Compost"])
    result["recommended_fertilizers"] = fertilizers

    # Also include explicit rule-based notes about N/P/K/pH/moisture (optional)
    notes = []
    N, P, K, pH, soil_moisture = values.flatten().tolist()
    if float(N) < 50:
        notes.append("Nitrogen low → consider Urea or organic N sources.")
    if float(P) < 40:
        notes.append("Phosphorus low → consider DAP or bone meal.")
    if float(K) < 40:
        notes.append("Potassium low → consider MOP (potash).")
    if float(pH) < 5.5:
        notes.append("Soil acidic → apply lime (after soil test).")
    if float(pH) > 7.5:
        notes.append("Soil alkaline → consider gypsum.")
    if float(soil_moisture) < 30:
        notes.append("Soil moisture low → irrigate before applying certain fertilizers.")

    result["notes"] = notes
    return result
