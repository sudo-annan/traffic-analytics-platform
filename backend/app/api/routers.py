from fastapi import APIRouter
from app.api.v1 import refresh, traffic, weather

# Main API router
api_router = APIRouter(prefix="/api/v1")

# Include individual route modules
api_router.include_router(refresh.router, tags=["Refresh"])
api_router.include_router(traffic.router, tags=["Traffic"])
api_router.include_router(weather.router, tags=["Weather"])