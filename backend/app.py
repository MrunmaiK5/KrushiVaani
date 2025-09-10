# backend/app.py
from fastapi import FastAPI
from backend.routes.fertilizer_routes import fertilizer_router
# import your crop router the same way:
from backend.routes.crop_routes import router as crop_router

app = FastAPI(title="Krushivaani API")

app.include_router(fertilizer_router, prefix="/api/fertilizer", tags=["Fertilizer"])
app.include_router(crop_router, prefix="/api/crop", tags=["Crop"])

@app.get("/")
def root():
    return {"message": "Welcome to Krushivaani API"}
