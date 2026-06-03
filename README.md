# 🌦️ Global Weather Pipeline & Analytics Platform

An end-to-end, high-performance data pipeline that extracts global meteorological forecast data, optimizes it using an embedded columnar database engine, and visualizes multi-continental weather patterns, dynamic alerts, and scientific correlations in real-time.

---

## 🛠️ System Architecture & Data Flow

The platform is engineered as a decoupled, three-tier data architecture optimized for speed, low memory footprints, and portable execution without external database server dependencies.

[Raw API Data (Open-Meteo)]
│ (HTTP Requests via Python Requests)
▼
[1. Extraction Layer (src/extract.py)]
│ (Writes highly compressed partitions)
▼
data/📂 /📂 /📂 /📂 /weather_HH-MM.parquet
│
│ (Blazing fast out-of-core streaming scan via DuckDB)
▼
[2. Transformation Layer (src/transform.py)]
│ (Deduplication, sorting, and analytical flattening)
▼
data/clean/daily/consolidat_daily.parquet
│
│ (Direct disk-to-dataframe queries)
▼
[3. Presentation Layer (Streamlit App)]
├── 🌦️ Overview & Geospatial Precipitation Map
├── 📊 Cross-City Thermal Comparisons
└── 🔬 Correlation Scientific Analytics (UV vs Temp)

[Raw API Data (Open-Meteo)]
│ (HTTP Requests via Python Requests)
▼
[1. Extraction Layer (src/extract.py)]
│ (Writes highly compressed partitions)
▼
data/📂 /📂 /📂 /📂 /weather_HH-MM.parquet
│
│ (Blazing fast out-of-core streaming scan via DuckDB)
▼
[2. Transformation Layer (src/transform.py)]
│ (Deduplication, sorting, and analytical flattening)
▼
data/clean/daily/consolidat_daily.parquet
│
│ (Direct disk-to-dataframe queries)
▼
[3. Presentation Layer (Streamlit App)]
├── 🌦️ Overview & Geospatial Precipitation Map
├── 📊 Cross-City Thermal Comparisons
└── 🔬 Correlation Scientific Analytics (UV vs Temp)

### Key Technology Stack Chosen
* **Storage Layer:** **Apache Parquet** (Columnar file layout ensuring high compression and projection pushdown capabilities).
* **Compute Engine:** **DuckDB** (An embedded vector-oriented OLAP database engine acting as our in-memory Data Warehouse layer).
* **Data Manipulation:** **Pandas** (Strictly utilized for lightweight schema mapping and final dataframe array structuring).
* **Frontend UI Engine:** **Streamlit & Altair** (Reactive web interface driving rapid interactive analytical graphs).

---

## 📂 Project Directory Structure

weather_pipeline/
├── data/
│   ├── clean/
│   │   └── daily/
│   │       └── consolidat_daily.parquet   # Consolidated operational analytics engine file
│   └── [City_Name]/                       # Dynamic partitioned cold storage directory
│       └── YYYY/MM/DD/weather_HH-MM.parquet
├── dashboard/
│   ├── overview.py                        # Live alerts and dynamic map rendering module
│   ├── comparison.py                      # Multi-city line and bar comparison analytics
│   └── correlation.py                     # Scientific Altair dual-axis UV tracking analysis
├── src/
│   ├── extract.py                         # API extraction pipeline orchestration script
│   └── transform.py                       # DuckDB-powered data consolidation logic
├── app.py                                 # Main system router and Streamlit navigation configuration
└── README.md                              # System operational manual

🚀 Getting Started & Execution Guide
1. Prerequisites & Environment Setup
Ensure your workspace is configured with Python 3.10+. Install the necessary pipeline framework dependencies using your terminal terminal package manager:

pip install streamlit pandas duckdb pyarrow requests altair

2. Running the Data PipelineExecute the stages chronologically to populate the analytic engine file:

Step 1: Trigger Data ExtractionFetches the latest 7-day meteorological snapshots across 42 global travel historical destinations.Bashpython src/extract.py

Step 2: Trigger Data Transformation & OptimizationLeverages DuckDB to scan all partitioned files, drops historical duplicate indices keeping the freshest forecast updates, and builds the analytical runtime layer.Bashpython src/transform.py

3. Launching the Dashboard InterfaceSpin up the presentation server using the local router:Bashstreamlit run app.py

🔬 Analytical Capabilities & Business Logic
🚨 Meteorological Automated Alert FrameworkThe dashboard analyzes live telemetry streams and applies thresholds bound to official meteorological hazards criteria:

Extreme Thermal Risks: Standardized thresholds flag severe cold waves ($T_{min} \le 0.0^\circ\text{C}$) or dangerous heat stress waves ($T_{max} \ge 35.0^\circ\text{C}$).

Flash Flood Routing Indicators: Active alerts flag heavy storm precipitation accumulations exceeding $30\text{ mm}$.

Gale Force Wind Indicators: Triggers safety warnings when systemic gusts surpass $50\text{ km/h}$.

Solar Radiation Vectors: Dynamic warnings highlight skin safety parameters whenever the maximum UV radiation threshold meets or exceeds $8.0\text{ UVI}$.

🗺️ Geospatial Precipitation Density
Map rendering utilizes an adaptive mathematical scaling expression bound to localized precipitation sums ($P_{sum}$) to drive variable visual cluster dimensions on screen dynamically:$$\text{Point Size} = (P_{sum} \times 50) + 50$$
This ensures permanent baseline visibility for geographic points reporting no rainfall while dynamically exaggerating storm centers.

🛡️ License & Project Specifications
API Data Provider Acknowledgement: Free meteorological datasets sourced directly from Open-Meteo Weather API (CC BY 4.0 license structure).Operational Scope: Global multi-region dataset tracking ($40+$ cities spanning Europe and North Africa).

### What makes this README great:
1. **Clear Visual Flow:** It includes an elegant ASCII-style text diagram mapping your exact input-output workflow.
2. **Advanced Details:** It references your structural layout (`data/clean/daily/consolidat_daily.parquet`), showing clean design practices.
3. **Mathematical Documentation:** Uses formal LaTeX notation to document how point sizes on your map are calculated and how safety alert thresholds are computed.