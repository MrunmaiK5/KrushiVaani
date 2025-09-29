from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Union
import sys
import os

# Add the backend directory to the Python path to import services
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from services.crop_service import recommend_crop

# Create router instance
router = APIRouter(prefix="/crop", tags=["crop"])

class CropRecommendationRequest(BaseModel):
    """Pydantic model for crop recommendation request validation"""
    N: Union[int, float] = Field(..., description="Nitrogen content in soil", ge=0, le=200)
    P: Union[int, float] = Field(..., description="Phosphorus content in soil", ge=0, le=200)
    K: Union[int, float] = Field(..., description="Potassium content in soil", ge=0, le=200)
    temperature: Union[int, float] = Field(..., description="Temperature in Celsius", ge=-50, le=60)
    humidity: Union[int, float] = Field(..., description="Humidity percentage", ge=0, le=100)
    ph: Union[int, float] = Field(..., description="Soil pH level", ge=0, le=14)
    rainfall: Union[int, float] = Field(..., description="Rainfall in mm", ge=0, le=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "N": 90,
                "P": 42,
                "K": 43,
                "temperature": 20.88,
                "humidity": 82.0,
                "ph": 6.5,
                "rainfall": 202.9
            }
        }

class CropRecommendationResponse(BaseModel):
    """Pydantic model for crop recommendation response"""
    recommended_crop: str = Field(..., description="The recommended crop based on input parameters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommended_crop": "rice"
            }
        }

@router.post("/recommend", response_model=CropRecommendationResponse)
async def recommend_crop_endpoint(request: CropRecommendationRequest):
    """
    Recommend a crop based on soil and environmental parameters.
    
    This endpoint accepts soil nutrient levels (N, P, K), environmental conditions 
    (temperature, humidity, pH, rainfall) and returns a crop recommendation.
    
    Args:
        request (CropRecommendationRequest): JSON payload containing:
            - N: Nitrogen content (0-200)
            - P: Phosphorus content (0-200) 
            - K: Potassium content (0-200)
            - temperature: Temperature in Celsius (-50 to 60)
            - humidity: Humidity percentage (0-100)
            - ph: Soil pH level (0-14)
            - rainfall: Rainfall in mm (0-1000)
    
    Returns:
        CropRecommendationResponse: JSON response containing the recommended crop
        
    Raises:
        HTTPException: 400 for invalid input parameters
        HTTPException: 500 for model loading or prediction errors
    """
    try:
        # Extract parameters from request
        params = {
            'N': request.N,
            'P': request.P,
            'K': request.K,
            'temperature': request.temperature,
            'humidity': request.humidity,
            'ph': request.ph,
            'rainfall': request.rainfall
        }
        
        # Call the crop recommendation service
        recommended_crop = recommend_crop(**params)
        
        # Return the response
        return CropRecommendationResponse(recommended_crop=recommended_crop)
        
    except ValueError as e:
        # Handle input validation errors
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input parameters: {str(e)}"
        )
    except FileNotFoundError as e:
        # Handle missing model files
        raise HTTPException(
            status_code=500,
            detail=f"Model files not found. Please ensure the model is trained and available: {str(e)}"
        )
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during crop recommendation: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the crop recommendation service is working.
    
    Returns:
        dict: Service status information
    """
    try:
        from services.crop_service import get_model_info
        model_info = get_model_info()
        
        if model_info['model_loaded']:
            return {
                "status": "healthy",
                "service": "crop_recommendation",
                "model_loaded": True,
                "model_type": model_info['model_type'],
                "features": model_info['feature_names']
            }
        else:
            return {
                "status": "unhealthy",
                "service": "crop_recommendation", 
                "model_loaded": False,
                "error": model_info.get('error', 'Unknown error')
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "crop_recommendation",
            "error": str(e)
        }

# Example usage documentation
"""
Example API Usage:

POST /crop/recommend
Content-Type: application/json

{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.88,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.9
}

Response:
{
    "recommended_crop": "rice"
}

Health Check:
GET /crop/health

Response:
{
    "status": "healthy",
    "service": "crop_recommendation",
    "model_loaded": true,
    "model_type": "RandomForestClassifier",
    "features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
}
"""
