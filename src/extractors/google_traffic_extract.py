#!/usr/bin/env python3
"""
google_traffic_extract.py
Single-city Google Maps visual extractor.
Usage:
  python3 google_traffic_extract.py --city "London" --lat 51.5074 --lon -0.1278
"""

import argparse
import json
import logging
import time
from datetime import datetime, UTC
from pathlib import Path

# re-use your existing code but accept args; simplified for single city
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import cv2
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True)
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--headless", action="store_true")
    return p.parse_args()

class GoogleMapsTrafficExtractor:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument('--headless=new')  # newer headless mode
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # optional
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.driver = uc.Chrome(options=options)
        try:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
        except Exception:
            pass
        logger.info("Chrome driver initialized")
        
    def navigate_to_location(self, lat, lng, zoom=13):
        try:
            url = f"https://www.google.com/maps/@{lat},{lng},{zoom}z"
            logger.info(f"Opening {url}")
            self.driver.get(url)
            time.sleep(6)  # let tiles load
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False

    def enable_traffic_layer(self):
        try:
            # Traffic button on Google maps may be inside a menu; we try multiple selectors
            # first try button with aria-label containing Traffic
            traffic_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Traffic']"))
            )
            traffic_button.click()
            time.sleep(3)
            logger.info("Traffic layer enabled")
            return True
        except Exception:
            # fallback: open menu and click "Traffic"
            try:
                # this is fragile; include try/except
                menu_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                for b in menu_buttons:
                    txt = b.get_attribute("aria-label") or ""
                    if "layers" in txt.lower() or "map type" in txt.lower():
                        b.click()
                        time.sleep(1)
                        # try to click traffic inside the menu
                        items = self.driver.find_elements(By.CSS_SELECTOR, "div[role='menuitem'], button")
                        for it in items:
                            if "traffic" in (it.text or "").lower():
                                it.click()
                                time.sleep(2)
                                return True
            except Exception:
                pass
        logger.warning("Could not enable traffic layer")
        return False

    def take_screenshot(self, out_path):
        try:
            # save full page screenshot; you can refine to crop map area later
            self.driver.save_screenshot(str(out_path))
            logger.info(f"Saved screenshot {out_path}")
            return str(out_path)
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None

    def analyze_traffic_colors(self, screenshot_path):
        try:
            image = cv2.imread(screenshot_path)
            if image is None:
                logger.error("Could not read screenshot")
                return None
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # HSV ranges tuned for Google Maps tones (may need tuning)
            red_lower1 = np.array([0, 100, 50]); red_upper1 = np.array([10, 255, 255])
            red_lower2 = np.array([160, 100, 50]); red_upper2 = np.array([180, 255, 255])
            yellow_lower = np.array([15, 80, 80]); yellow_upper = np.array([35, 255, 255])
            green_lower = np.array([35, 50, 50]); green_upper = np.array([90, 255, 255])

            red_mask = cv2.bitwise_or(cv2.inRange(hsv, red_lower1, red_upper1),
                                      cv2.inRange(hsv, red_lower2, red_upper2))
            yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
            green_mask = cv2.inRange(hsv, green_lower, green_upper)

            total_pixels = image.shape[0] * image.shape[1]
            red_pixels = int(cv2.countNonZero(red_mask))
            yellow_pixels = int(cv2.countNonZero(yellow_mask))
            green_pixels = int(cv2.countNonZero(green_mask))

            red_pct = (red_pixels / total_pixels) * 100
            yellow_pct = (yellow_pixels / total_pixels) * 100
            green_pct = (green_pixels / total_pixels) * 100

            congestion_score = (red_pct * 1.0 + yellow_pct * 0.5 + green_pct * 0.1)

            return {
                "red_percentage": round(red_pct, 3),
                "yellow_percentage": round(yellow_pct, 3),
                "green_percentage": round(green_pct, 3),
                "congestion_score": round(congestion_score, 3),
                "total_pixels": total_pixels
            }
        except Exception as e:
            logger.error(f"Color analysis error: {e}")
            return None

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception:
            pass

def main():
    args = parse_args()
    city = args.city
    lat = args.lat
    lon = args.lon
    headless = args.headless

    processed_dir = Path(__file__).resolve().parents[2] / "data" / "google" / "processed"
    raw_dir = Path(__file__).resolve().parents[2] / "data" / "google" / "raw"
    processed_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    ext = GoogleMapsTrafficExtractor(headless=headless)
    try:
        ok = ext.navigate_to_location(lat, lon, zoom=13)
        if not ok:
            logger.error("Navigation failed, aborting")
            return 2

        ext.enable_traffic_layer()
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{city.replace(' ','_')}_{timestamp}.png"
        screenshot_path = processed_dir / screenshot_name
        ss = ext.take_screenshot(screenshot_path)
        if not ss:
            logger.error("Screenshot failed")
            return 3

        analysis = ext.analyze_traffic_colors(str(screenshot_path))
        if not analysis:
            logger.error("Analysis failed")
            return 4

        # Build combined result for single-city single-run (we treat one 'route' = whole view)
        result = {
            "extraction_timestamp": datetime.now(UTC).isoformat(),
            "city": city,
            "lat": lat,
            "lon": lon,
            "results": [
                {
                    "route_name": f"{city} - view",
                    "timestamp": datetime.now(UTC).isoformat(),
                    "location": f"{lat},{lon}",
                    "congestion_percentage": min(100, analysis["congestion_score"] * 2),  # scale
                    "average_delay_minutes": max(0, analysis["congestion_score"] * 0.5),
                    "traffic_level": "Severe" if analysis["congestion_score"] > 7 else "Moderate" if analysis["congestion_score"] > 3 else "Light",
                    "color_breakdown": {
                        "red": analysis["red_percentage"],
                        "yellow": analysis["yellow_percentage"],
                        "green": analysis["green_percentage"]
                    },
                    "extraction_method": "visual_analysis",
                    "screenshot_path": str(screenshot_path)
                }
            ]
        }

        out_file = processed_dir / f"combined_{city.replace(' ','_')}_{timestamp}.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)

        logger.info(f"Saved processed google traffic file: {out_file}")
        print(out_file)
        return 0

    finally:
        ext.close()

if __name__ == "__main__":
    exit(main())
