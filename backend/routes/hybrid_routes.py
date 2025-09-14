from fastapi import APIRouter, HTTPException
from backend.services.crop_service import predict_crop
from backend.services.fertilizer_service import recommend_fertilizer

hybrid_router = APIRouter()

@hybrid_router.post("/recommend_crop_and_fertilizer")
def recommend_all(data: dict):
    try:
        # Step 1: Predict crop using ML
        crop_result = predict_crop(data)

        # Step 2: Add predicted crop to input data
        data["Crop"] = crop_result["predicted_crop"]

        # Step 3: Get fertilizer recommendation using rule-based service
        fertilizer_result = recommend_fertilizer(data)

        # Step 4: Return both results in one response
        return {
            "crop": crop_result,
            "fertilizer": fertilizer_result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
