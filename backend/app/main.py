from fastapi import FastAPI
from app.api import traffic, metrics, weather
from app.api.weather import router as weather_router
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Create tables (if not already created)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Traffic Data API")

# ✅ Allow requests from your React frontend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allowed frontend origins
    allow_credentials=True,
    allow_methods=["*"],             # Allow all HTTP methods
    allow_headers=["*"],             # Allow all headers
)


# Register routers
app.include_router(traffic.router)
app.include_router(metrics.router)

app.include_router(weather.router)

@app.get("/")
def root():
    return {"message": "Traffic Data API is running"}
