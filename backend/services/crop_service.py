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
            raise FileNotFoundError(
                f"Model files not found. Ensure 'crop_model.pkl' and 'feature_names.pkl' exist. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    return _crop_model, _feature_names


def recommend_crop(N: Union[int, float], P: Union[int, float], K: Union[int, float],
                   temperature: Union[int, float], humidity: Union[int, float],
                   ph: Union[int, float], rainfall: Union[int, float]) -> str:
    """Recommend crop based on soil & environmental parameters."""
    try:
        model, feature_names = _load_model()

        input_data = pd.DataFrame([{'N': N, 'P': P, 'K': K, 'temperature': temperature, 'humidity': humidity, 'ph': ph,
                                    'rainfall': rainfall}])
        input_data = input_data[feature_names]
        prediction = model.predict(input_data)
        return str(prediction[0])
    except Exception as e:
        raise Exception(f"Failed to recommend crop: {str(e)}")


def predict_crop(input_data: dict) -> dict:
    """Hybrid-friendly crop prediction function."""
    try:
        required_keys = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Missing required field: {key}")

        recommended = recommend_crop(
            N=input_data['N'], P=input_data['P'], K=input_data['K'],
            temperature=input_data['temperature'], humidity=input_data['humidity'],
            ph=input_data['ph'], rainfall=input_data['rainfall']
        )
        return {"predicted_crop": recommended}
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid or missing field in input data: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to predict crop: {str(e)}")