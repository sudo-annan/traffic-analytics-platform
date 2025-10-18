from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import refresh, traffic, weather
from app.database import Base, engine

app = FastAPI(title="Traffic Analytics API")

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

Base.metadata.create_all(bind=engine)

app.include_router(refresh.router)
app.include_router(traffic.router)
app.include_router(weather.router)
