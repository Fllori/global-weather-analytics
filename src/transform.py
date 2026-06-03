from pathlib import Path
import duckdb
import pandas as pd

def transform_weather_data():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    raw_dir = project_root / "data" / "1_raw"
    trusted_dir = project_root / "data" / "2_trusted"
    trusted_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== [ETL: TRANSFORM] Initiating data aggregation and deduplication ===")
    
    if not raw_dir.exists():
        print("[Notice] Directory 1_raw does not exist. Pipeline idle.")
        return

    # Check for raw forecast files in the path topology tree
    all_raw_files = list(raw_dir.rglob("raw_forecast.parquet"))
    if not all_raw_files:
        print("[Notice] No new raw files discovered in 1_raw for transformation.")
        return

    try:
        # Scan everything using the unified Hive file pattern template
        raw_pattern = str(raw_dir / "an=*" / "luna=*" / "zi=*" / "raw_forecast.parquet")
        
        # High-performance DuckDB query execution directly on file assets
        df_consolidated = duckdb.query(f"SELECT * FROM '{raw_pattern}'").df()
        
        # Smart Deduplication: Keep the most recent extraction for overlapping forecasts
        df_consolidated = df_consolidated.sort_values(by="extracted_at")
        df_consolidated = df_consolidated.drop_duplicates(
            subset=["time", "oras_nume"], 
            keep="last"
        )
        
        # Extract calendar components for faster queries downstream
        df_consolidated["time_parsed"] = pd.to_datetime(df_consolidated["time"])
        df_consolidated["an"] = df_consolidated["time_parsed"].dt.strftime("%Y")
        df_consolidated["luna"] = df_consolidated["time_parsed"].dt.strftime("%m")
        df_consolidated["zi"] = df_consolidated["time_parsed"].dt.strftime("%d")
        df_consolidated = df_consolidated.drop(columns=["time_parsed"])
        
        # Logical analytical sort
        df_consolidated = df_consolidated.sort_values(
            by=["an", "luna", "zi", "tara_nume", "oras_nume"]
        ).reset_index(drop=True)
        
        # Serialize to Trusted zone
        output_file = trusted_dir / "daily_consolidated.parquet"
        df_consolidated.to_parquet(output_file, engine="pyarrow", index=False)
        
        print(f"-> [Transform-Ok] Consolidated and deduplicated file at: {output_file.relative_to(project_root)}")
        print("=== [ETL: TRANSFORM] Completed successfully! ===\n")
        
    except Exception as err:
        print(f"[Transform-Fail] Critical runtime failure during stage: {err}")

if __name__ == "__main__":
    transform_weather_data()