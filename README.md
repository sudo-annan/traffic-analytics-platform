# 🚦 Traffic Analytics Platform

An end-to-end system to extract, process, and visualize real-time traffic and weather data for London.

## 🧱 Architecture

**Tech stack:**  
- FastAPI (backend REST API)  
- PostgreSQL (data persistence)  
- React (frontend dashboard)  
- Docker (deployment)  
- Data sources: TfL Unified API, OpenWeatherMap API

## 📂 Repository Structure

traffic-analytics-platform/
│
├── src/ # Extractors + ETL
├── backend/ # FastAPI backend
├── frontend/ # React frontend (to be added)
├── docker/ # Deployment setup
└── data/ # Stored JSONs (raw + processed)


## 🚀 Setup

```bash
git clone https://github.com/<your-username>/traffic-analytics-platform.git
cd traffic-analytics-platform
bash scripts/setup.sh
