import os
import glob
import logging
from pathlib import Path

def cleanup_old_files(processed_dir: Path, city: str, keep_latest: int = 1):
    """
    Deletes old processed files (.json, .png) for a given city, keeping only the latest ones.

    Args:
        processed_dir (Path): Directory containing processed files.
        city (str): City name used in filenames (case-insensitive match).
        keep_latest (int): Number of most recent files to keep (default=1).
    """
    if not processed_dir.exists():
        logging.warning(f"Cleanup skipped — directory does not exist: {processed_dir}")
        return

    # Normalize city pattern (case-insensitive)
    city_pattern = city.replace(" ", "_").lower()

    # Collect all matching JSON and PNG files
    all_files = []
    for ext in ("json", "png"):
        all_files.extend(glob.glob(str(processed_dir / f"*{city_pattern}*.{ext}")))

    if not all_files:
        logging.info(f"No old files to clean for city: {city}")
        return

    # Sort by modification time (oldest first)
    all_files.sort(key=lambda f: os.path.getmtime(f))

    # Determine files to delete
    if keep_latest > 0:
        to_delete = all_files[:-keep_latest]
    else:
        to_delete = all_files

    # Delete files
    for f in to_delete:
        try:
            os.remove(f)
            logging.info(f"🧹 Deleted old file: {f}")
        except Exception as e:
            logging.warning(f"Failed to delete {f}: {e}")

    logging.info(f"✅ Cleanup complete for {city}: kept {keep_latest}, deleted {len(to_delete)} files.")
