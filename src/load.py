from pathlib import Path
import pandas as pd

def load_weather_data():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    trusted_file = project_root / "data" / "2_trusted" / "daily_consolidated.parquet"
    load_dir = project_root / "data" / "3_load"
    load_dir.mkdir(parents=True, exist_ok=True)
    
    target_mart_file = load_dir / "weather_mart.parquet"
    
    print("=== [ETL: LOAD] Loading clean assets into Production Data Mart ===")
    
    if not trusted_file.exists():
        print(f"[Critical Error] Target file missing from Trusted layer: {trusted_file}")
        return

    try:
        # Load verified data records from the Trusted layer
        df = pd.read_parquet(trusted_file)
        
        # Strip away technical operational metadata before frontend presentation serving
        if "extracted_at" in df.columns:
            df = df.drop(columns=["extracted_at"])
            
        # Write out optimized reporting Data Mart file
        df.to_parquet(target_mart_file, engine="pyarrow", index=False)
        
        print(f"-> [Load-Ok] Platform updated. Production Data Mart ready at: {target_mart_file.relative_to(project_root)}")
        print("=== [ETL: LOAD] Full ETL Pipeline finished successfully! ===\n")
        
    except Exception as err:
        print(f"[Load-Fail] Failed to push data assets into production: {err}")

if __name__ == "__main__":
    load_weather_data()