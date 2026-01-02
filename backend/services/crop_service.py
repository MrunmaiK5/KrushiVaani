<<<<<<< HEAD
=======
# import pandas as pd
# import joblib
# import os

# _crop_model = None
# _feature_names = None

# def _load_model():
#     """Load the trained crop model and feature names (with caching)."""
#     global _crop_model, _feature_names
#     if _crop_model is None:
#         try:
#             # Construct path relative to the project root or use absolute paths
#             model_path = os.path.join('ml_models', 'crop_recommendation', 'crop_model.pkl')
#             feature_names_path = os.path.join('ml_models', 'crop_recommendation', 'feature_names.pkl')
#             _crop_model = joblib.load(model_path)
#             _feature_names = joblib.load(feature_names_path)
#         except FileNotFoundError as e:
#             raise FileNotFoundError(f"Crop model files not found. Error: {e}")
#         except Exception as e:
#              raise Exception(f"Error loading crop model: {e}")
#     return _crop_model, _feature_names

# def recommend_crop(input_data: dict) -> str:
#     """Recommend crop based on a dictionary of soil & environmental parameters."""
#     try:
#         model, feature_names = _load_model()
        
#         required_keys = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
#         # Check if all required keys are present in the input dictionary
#         for key in required_keys:
#             if key not in input_data:
#                 raise ValueError(f"Missing required field for crop prediction: {key}")

#         # Create a DataFrame from the input dictionary
#         df = pd.DataFrame([input_data])
#         # Reorder columns to match the training order
#         df = df[feature_names] 
        
#         prediction = model.predict(df)
#         return str(prediction[0])
#     except ValueError as e:
#          # Reraise ValueError specifically for frontend clarity
#          raise ValueError(str(e))
#     except Exception as e:
#         raise Exception(f"Failed to recommend crop: {str(e)}")

>>>>>>> c1a451279ad8528d78550fa2f59895c93599359a
import pandas as pd
import joblib
import os

_crop_model = None
_feature_names = None

def _load_model():
    """Load the trained crop model and feature names using robust absolute pathing."""
    global _crop_model, _feature_names
    if _crop_model is None:
        try:
            # Gets the absolute path to backend/services/
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            
            # Navigates up to KrushiVaani/ root and then into the specific ML folder
            model_path = os.path.abspath(os.path.join(
                BASE_DIR, '..', '..', 'ml_models', 'crop_recommendation', 'crop_model.pkl'
            ))
            feature_names_path = os.path.abspath(os.path.join(
                BASE_DIR, '..', '..', 'ml_models', 'crop_recommendation', 'feature_names.pkl'
            ))

            # Debug print to verify the path in your terminal
            print(f"DEBUG: Attempting to load Crop model from: {model_path}")

            if not os.path.exists(model_path):
                 raise FileNotFoundError(f"Model file missing at: {model_path}. Verify your KrushiVaani folder structure.")

            _crop_model = joblib.load(model_path)
            _feature_names = joblib.load(feature_names_path)
            
        except Exception as e:
            raise Exception(f"Failed to load crop model: {str(e)}")
            
    return _crop_model, _feature_names

def recommend_crop(input_data: dict) -> str:
    """Recommend crop based on soil and environmental parameters."""
    try:
        model, feature_names = _load_model()

        # Ensure keys match your Random Forest features exactly
        required_keys = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for key in required_keys:
            if key not in input_data:
                # Provide a default value to prevent code from crashing if data is missing
                input_data[key] = 0.0

        # Create DataFrame for prediction using the loaded feature names
        df = pd.DataFrame([input_data])[feature_names]
        prediction = model.predict(df)
        
        return str(prediction[0])
    except Exception as e:
        raise Exception(f"Failed to recommend crop: {str(e)}")