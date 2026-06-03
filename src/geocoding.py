import json
from pathlib import Path
import time
import requests

# Clean, simple list of raw target destinations (No coordinates needed!)
# Enriched target destinations with explicit country hints to prevent API cross-continental mismatch
CITIES_TO_CATALOG = [
    "Saints Constantine and Helena, Bulgaria", "Varna, Bulgaria", "Budapest, Hungary", "Gyor, Hungary", 
    "Rome, Italy", "Bari, Italy", "Polignano a Mare, Italy", "Naples, Italy", "Sorrento, Italy", 
    "Positano, Italy", "Amalfi, Italy", "Milan, Italy", "Bergamo, Italy", "Verona, Italy", 
    "Matera, Italy", "Monopoli, Italy", "Brescia, Italy", "Sirmione, Italy", "Brixen, Italy", 
    "Munich, Germany", "Prague, Czech Republic", "Brno, Czech Republic", "Vienna, Austria", 
    "Bratislava, Slovakia", "Zakynthos, Greece", "Lefkada, Greece", "Kefalonia, Greece", 
    "Malmo, Sweden", "Copenhagen, Denmark", "Krakow, Poland", "Zakopane, Poland", 
    "Nis, Serbia", "Skopje, North Macedonia", "Barcelona, Spain", "Castello de la Plana, Spain", 
    "Valencia, Spain", "Nice, France", "Antibes, France", "Monaco, France", "Eze, France", 
    "Paris, France", "Lyon, France", "Hurghada, Egypt", "London, United Kingdom", "Rotterdam, Netherlands"
]

def build_city_geocoding_catalog():
    """
    Queries the public Open-Meteo Geocoding API to dynamically build an enriched
    JSON catalog containing coordinates, countries, and regional metadata.
    """
    project_root = Path(__file__).resolve().parent.parent
    config_dir = project_root / "config"
    config_dir.mkdir(exist_ok=True)
    output_catalog_path = config_dir / "cities_catalog.json"
    
    catalog = []
    print("=== Initiating Dynamic Geocoding Catalog Generation ===")
    
    for city_name in CITIES_TO_CATALOG:
        print(f"Resolving coordinates and metadata for: '{city_name}'...")
        
        # Open-Meteo Geocoding Endpoint
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                
                # Extract core coordinates along with extra dynamic metadata attributes
                city_entry = {
                    "name": result["name"],
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "country": result.get("country", "Unknown"),
                    "country_code": result.get("country_code", "XX"),
                    "timezone": result.get("timezone", "UTC"),
                    "elevation_meters": result.get("elevation", 0.0)
                }
                catalog.append(city_entry)
                print(f"-> Found: {city_entry['name']}, {city_entry['country']} [{city_entry['timezone']}]")
            else:
                print(f"[Warning] No geocoding match discovered on map for lookup: '{city_name}'")
                
            # Respectful API pacing delay
            time.sleep(0.3)
            
        except Exception as err:
            print(f"[Error] Failed to fetch geocoding payload matrix for '{city_name}': {err}")
            
    # Serialize metadata block into an indented, clean configuration layout
    with open(output_catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)
        
    print(f"\n--- Catalog Generation Complete! Saved {len(catalog)} entries to config/cities_catalog.json ---\n")

if __name__ == "__main__":
    build_city_geocoding_catalog()