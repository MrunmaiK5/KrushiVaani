import pandas as pd
import joblib
import os
from typing import Union

# Global variable to store the loaded model (for caching)
_crop_model = None
_feature_names = None

def _load_model():
    """
    Load the trained crop recommendation model and feature names.
    Uses caching to avoid reloading the model on every prediction.
    """
    global _crop_model, _feature_names
    
    if _crop_model is None or _feature_names is None:
        try:
            # Get the path to the model files relative to this service
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            model_path = os.path.join(project_root, 'ml_models', 'crop_recommendation', 'crop_model.pkl')
            feature_names_path = os.path.join(project_root, 'ml_models', 'crop_recommendation', 'feature_names.pkl')
            
            # Load the model and feature names
            _crop_model = joblib.load(model_path)
            _feature_names = joblib.load(feature_names_path)
            
            print(f"Model loaded successfully from: {model_path}")
            print(f"Feature names loaded: {_feature_names}")
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Model files not found. Please ensure crop_model.pkl and feature_names.pkl exist in ml_models/crop_recommendation/. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    return _crop_model, _feature_names

def recommend_crop(N: Union[int, float], P: Union[int, float], K: Union[int, float], 
                  temperature: Union[int, float], humidity: Union[int, float], 
                  ph: Union[int, float], rainfall: Union[int, float]) -> str:
    """
    Recommend a crop based on soil and environmental parameters.
    
    Args:
        N (int/float): Nitrogen content in soil
        P (int/float): Phosphorus content in soil  
        K (int/float): Potassium content in soil
        temperature (int/float): Temperature in Celsius
        humidity (int/float): Humidity percentage
        ph (int/float): Soil pH level
        rainfall (int/float): Rainfall in mm
        
    Returns:
        str: Recommended crop name
        
    Raises:
        ValueError: If any input parameter is invalid
        FileNotFoundError: If model files are not found
        Exception: If prediction fails
    """
    try:
        # Validate input parameters
        input_params = [N, P, K, temperature, humidity, ph, rainfall]
        param_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
        for param, name in zip(input_params, param_names):
            if not isinstance(param, (int, float)):
                raise ValueError(f"{name} must be a number, got {type(param).__name__}")
            if pd.isna(param):
                raise ValueError(f"{name} cannot be NaN or None")
        
        # Load the model and feature names
        model, feature_names = _load_model()
        
        # Prepare input data as DataFrame
        input_data = pd.DataFrame({
            'N': [N],
            'P': [P], 
            'K': [K],
            'temperature': [temperature],
            'humidity': [humidity],
            'ph': [ph],
            'rainfall': [rainfall]
        })
        
        # Ensure columns are in the correct order
        input_data = input_data[feature_names]
        
        # Make prediction
        prediction = model.predict(input_data)
        
        # Return the predicted crop as string
        recommended_crop = prediction[0]
        
        print(f"Input parameters: N={N}, P={P}, K={K}, temp={temperature}, humidity={humidity}, ph={ph}, rainfall={rainfall}")
        print(f"Recommended crop: {recommended_crop}")
        
        return recommended_crop
        
    except ValueError as e:
        print(f"Input validation error: {str(e)}")
        raise
    except FileNotFoundError as e:
        print(f"Model file error: {str(e)}")
        raise
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise Exception(f"Failed to make crop recommendation: {str(e)}")

def get_model_info() -> dict:
    """
    Get information about the loaded model.
    
    Returns:
        dict: Model information including feature names and model type
    """
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

# Example usage and testing
if __name__ == "__main__":
    # Test the function with sample data
    try:
        # Sample input (you can modify these values for testing)
        sample_input = {
            'N': 90,
            'P': 42, 
            'K': 43,
            'temperature': 20.88,
            'humidity': 82.0,
            'ph': 6.5,
            'rainfall': 202.9
        }
        
        print("Testing crop recommendation service...")
        print(f"Sample input: {sample_input}")
        
        recommended = recommend_crop(**sample_input)
        print(f"Recommended crop: {recommended}")
        
        # Get model info
        model_info = get_model_info()
        print(f"Model info: {model_info}")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
