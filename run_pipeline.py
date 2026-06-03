import subprocess
import sys
from pathlib import Path

def run_script(script_path):
    print(f"\n[Executing] {script_path}...")
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        print(f"[Error] Script {script_path} failed with exit code {result.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent
    
    # Define execution sequence for the formal ETL pipeline
    geocoding_script = root_dir / "src" / "geocoding.py"
    extract_script = root_dir / "src" / "extract.py"
    transform_script = root_dir / "src" / "transform.py"
    load_script = root_dir / "src" / "load.py"
    
    print("==================================================")
    print("        STARTING METEOROLOGICAL ETL PIPELINE     ")
    print("==================================================")
    
    catalog_file = root_dir / "config" / "cities_catalog.json"
    if not catalog_file.exists():
        run_script(geocoding_script)
    else:
        print("[Skipping] City geocoding catalog already exists.")
        
    # Sequential execution control of the ETL components
    run_script(extract_script)   # Extract (E)
    run_script(transform_script) # Transform (T)
    run_script(load_script)      # Load (L)
    
    print("==================================================")
    print("Pipeline synchronized! Launching Streamlit UI layer...")
    print("==================================================")
    
    try:
        subprocess.run(["streamlit", "run", str(root_dir / "app.py")])
    except KeyboardInterrupt:
        print("\nDashboard server shutdown successfully.")