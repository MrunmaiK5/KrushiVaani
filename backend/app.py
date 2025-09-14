# backend/app.py
from fastapi import FastAPI
from backend.routes.fertilizer_routes import fertilizer_router
from backend.routes.crop_routes import router as crop_router
from backend.routes.hybrid_routes import hybrid_router  # new hybrid endpoint

app = FastAPI(title="Krushivaani API")

# Include individual routers
app.include_router(fertilizer_router, prefix="/api/fertilizer", tags=["Fertilizer"])
app.include_router(crop_router, prefix="/api/crop", tags=["Crop"])
app.include_router(hybrid_router, prefix="/api/hybrid", tags=["Hybrid"])  # Hybrid flow

@app.get("/")
def root():
    return {"message": "Welcome to Krushivaani API"}
