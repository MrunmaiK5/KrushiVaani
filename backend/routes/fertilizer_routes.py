from fastapi import APIRouter
from services.fertilizer_service import recommend_fertilizer

fertilizer_router = APIRouter()

@fertilizer_router.post("/recommend")
def recommend(data: dict):
    result = recommend_fertilizer(data)
    return {"recommendation": result}
