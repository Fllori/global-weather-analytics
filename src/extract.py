from datetime import datetime
import json
from pathlib import Path
import pandas as pd
import requests

# Configure project route topology
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
catalog_path = project_root / "config" / "cities_catalog.json"
raw_stage_dir = project_root / "data" / "1_raw"

# Generate timestamp components for Hive Partitioning
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

def extract_weather_data():
    if not catalog_path.exists():
        print("[Critical Error] Catalog configuration file missing!")
        print("Please run 'python src/geocoding.py' first.")
        return

    with open(catalog_path, "r", encoding="utf-8") as f:
        cities = json.load(f)

    print(f"=== [ETL: EXTRACT] Extracting raw weather metrics for {len(cities)} cities ===")
    
    all_cities_frames = []

    for city in cities:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={city['latitude']}"
            f"&longitude={city['longitude']}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,uv_index_max,wind_speed_10m_max"
            f"&timezone={city['timezone'].replace('/', '%2F')}"
        )
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            payload = response.json()
            
            df = pd.DataFrame(payload["daily"])
            
            # Append dynamic lineage tracking metadata
            df["oras_nume"] = city["name"]
            df["latitude"] = city["latitude"]
            df["longitude"] = city["longitude"]
            df["tara_nume"] = city["country"]
            df["country_code"] = city["country_code"]
            df["extracted_at"] = now
            
            all_cities_frames.append(df)
            print(f"-> [Extract-Fetch] Metrics captured successfully for: {city['name']}")
            
        except requests.exceptions.RequestException as req_err:
            print(f"[API Network Error] Connection dropped for {city['name']}: {req_err}")
        except Exception as err:
            print(f"[Pipeline Runtime Error] Failed to process mapping data for {city['name']}: {err}")

    # Unitary storage execution if raw chunks were collected
    if all_cities_frames:
        df_global_raw = pd.concat(all_cities_frames, ignore_index=True)
        
        # Optimal Data Engineering Hive Partitioning structure (Time governs hierarchy)
        target_folder = raw_stage_dir / f"an={year}" / f"luna={month}" / f"zi={day}"
        target_folder.mkdir(parents=True, exist_ok=True)
        
        file_path = target_folder / "raw_forecast.parquet"
        
        # Enforce formal execution layout index matching
        column_order = [
            "oras_nume", "latitude", "longitude", "tara_nume", "country_code",
            "time", "temperature_2m_max", "temperature_2m_min", 
            "precipitation_sum", "uv_index_max", "wind_speed_10m_max", "extracted_at"
        ]
        df_global_raw = df_global_raw[column_order]
        
        df_global_raw.to_parquet(file_path, engine="pyarrow", index=False)
        print(f"\n=== [ETL: EXTRACT] Success! Global raw asset saved at: {file_path.relative_to(project_root)} ===")
    else:
        print("[Extract-Warning] No data payloads were collected from the API.")

if __name__ == "__main__":
    extract_weather_data()