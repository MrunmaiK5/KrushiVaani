# backend/services/crop_service.py
import pandas as pd
import joblib
import os
from typing import Union

# Global variables for caching
_crop_model = None
_feature_names = None

def _load_model():
    """Load the trained crop model and feature names (with caching)."""
    global _crop_model, _feature_names
    if _crop_model is None or _feature_names is None:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            model_path = os.path.join(project_root, 'ml_models', 'crop_recommendation', 'crop_model.pkl')
            feature_names_path = os.path.join(project_root, 'ml_models', 'crop_recommendation', 'feature_names.pkl')
            
            _crop_model = joblib.load(model_path)
            _feature_names = joblib.load(feature_names_path)
            
            print(f"Model loaded from: {model_path}")
            print(f"Features: {_feature_names}")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Model files not found. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    return _crop_model, _feature_names

def recommend_crop(N: Union[int, float], P: Union[int, float], K: Union[int, float],
                  temperature: Union[int, float], humidity: Union[int, float],
                  ph: Union[int, float], rainfall: Union[int, float]) -> str:
    """Recommend crop based on soil & environmental parameters."""
    try:
        # Validate inputs
        input_params = [N, P, K, temperature, humidity, ph, rainfall]
        param_names = ['N','P','K','temperature','humidity','ph','rainfall']
        for param, name in zip(input_params, param_names):
            if not isinstance(param, (int, float)):
                raise ValueError(f"{name} must be number, got {type(param).__name__}")
            if pd.isna(param):
                raise ValueError(f"{name} cannot be NaN")
        
        model, feature_names = _load_model()
        
        input_data = pd.DataFrame([{
            'N': N, 'P': P, 'K': K,
            'temperature': temperature, 'humidity': humidity,
            'ph': ph, 'rainfall': rainfall
        }])
        
        input_data = input_data[feature_names]  # ensure correct column order
        prediction = model.predict(input_data)
        return str(prediction[0])
    except Exception as e:
        raise Exception(f"Failed to recommend crop: {str(e)}")

def predict_crop(input_data: dict) -> dict:
    """
    Hybrid-friendly crop prediction function.
    input_data: dict with keys ['N','P','K','temperature','humidity','ph','rainfall']
    returns: dict {"predicted_crop": "<crop_name>"}
    """
    try:
        recommended_crop = recommend_crop(
            N=input_data['N'],
            P=input_data['P'],
            K=input_data['K'],
            temperature=input_data['temperature'],
            humidity=input_data['humidity'],
            ph=input_data['ph'],
            rainfall=input_data['rainfall']
        )
        return {"predicted_crop": recommended_crop}
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to predict crop: {str(e)}")

def get_model_info() -> dict:
    """Return info about loaded crop model."""
    try:
        model, feature_names = _load_model()
        return {
            'model_type': type(model).__name__,
            'feature_names': feature_names,
            'n_features': len(feature_names),
            'model_loaded': True
        }
    except Exception as e:
        return {
            'model_type': None,
            'feature_names': None,
            'n_features': 0,
            'model_loaded': False,
            'error': str(e)
        }

# Example test
if __name__ == "__main__":
    sample_input = {
        'N': 90, 'P': 42, 'K': 43,
        'temperature': 20.88, 'humidity': 82.0,
        'ph': 6.5, 'rainfall': 202.9
    }
    print("Predicted crop:", predict_crop(sample_input))
