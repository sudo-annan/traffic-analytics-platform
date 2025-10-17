import subprocess
from pathlib import Path

def refresh_tfl_data():
    """
    Re-runs TfL + Weather extractors and ETL loaders.
    """
    try:
        project_root = Path(__file__).resolve().parents[3]

        # --- Traffic ---
        extractor_tfl = project_root / "src" / "extractors" / "tfl_extract.py"
        loader_tfl = project_root / "src" / "etl" / "etl_tfl_loader.py"

        # --- Weather ---
        extractor_weather = project_root / "src" / "extractors" / "weather_extract.py"
        loader_weather = project_root / "src" / "etl" / "etl_weather_loader.py"

        subprocess.run(["python3", str(extractor_tfl)], check=True)
        subprocess.run(["python3", str(loader_tfl)], check=True)
        subprocess.run(["python3", str(extractor_weather)], check=True)
        subprocess.run(["python3", str(loader_weather)], check=True)

        return True, "Traffic & Weather refresh successful."
    except subprocess.CalledProcessError as e:
        return False, f"Refresh failed: {e}"
