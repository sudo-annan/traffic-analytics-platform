from fastapi import FastAPI
from app.config import settings
from app.cors import setup_cors
from app.api.routers import api_router

app = FastAPI(
    title="Traffic Analytics API",
    description="API for traffic and weather data analytics",
    version="1.0.0"
)

# Setup CORS
setup_cors(app)

# Include all API routes
app.include_router(api_router)