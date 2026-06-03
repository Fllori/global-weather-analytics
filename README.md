# 🌦️ Global Weather Analytics & GenAI Vacation Concierge

An advanced, end-to-end data platform and interactive dashboard built to clean, process, and visualize localized historical weather metrics and predictive solar radiation risks across European destinations. The application features a synchronized multi-page layout and integrates **Google Gemini AI** to provide custom, real-time lifestyle itineraries and travel safety advisories.

## 🚀 Core Features

- **🗺️ Interactive Geospatial Mapping:** Clean, adaptive visualization of European weather trends utilizing a customized tokenless Dark Matter PyDeck layout with dynamically scaled pixel-radius bubbles representing localized precipitation.
- **🔄 Synchronized Multi-Page Architecture:** State-retaining sidebar filters powered by `st.session_state`. Selecting a country or city on one page locks the preference seamlessly across all tabs without widget reset faults.
- **📊 Solar Radiation & UV Safety Profiles:** Advanced analytical charts mapping ultraviolet radiation metrics (`uv_index_max`) directly against official World Health Organization (WHO) biological risk categories.
- **🤖 GenAI Vacation Concierge:** Automated integration with the native Google GenAI SDK (`gemini-2.5-flash`), delivering 3 highly specific, contextualized outdoor and safety recommendations tailored to the selected city's exact meteorological conditions.

## 🛠️ Tech Stack & Architecture

- **Frontend Dashboard:** [Streamlit](https://streamlit.io/) (Multi-page configuration via `st.navigation`)
- **Data Query Engine:** [DuckDB](https://duckdb.org/) (High-performance analytical in-memory storage parsing production assets)
- **Geospatial Processing:** [PyDeck](https://deckgl.github.io/pydeck/) (Scatterplot presentation layers with dynamic float constraints)
- **Data Wrangling:** [Pandas](https://pandas.pydata.org/) & [Apache Parquet](https://parquet.apache.org/) (Columnar storage optimization)
- **Generative AI:** [Google GenAI SDK](https://github.com/google/generative-ai-python) (`gemini-2.5-flash` model layer)

---

## 💻 Installation & Local Setup

Follow these steps to configure your environment and deploy the dashboard locally:

1. Clone the Repository
```bash
git clone [https://github.com/Fllori/global-weather-analytics.git](https://github.com/Fllori/global-weather-analytics.git)
cd global-weather-analytics

2. Configure Virtual Environment (Recommended)
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate

3. Install Dependencies
pip install streamlit duckdb pandas pydeck altair google-genai

4. Secure Secrets Management
To ensure safe operations on Git and prevent API Token leakage, local configurations are isolated. Create a credentials store under .streamlit/secrets.toml (this file is excluded via .gitignore):
# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"

5. Launch the Framework Dashboard
Execute the central entry point orchestration layer:
streamlit run app.py

📁 Project Structure
global-weather-analytics/
├── .streamlit/
│   └── secrets.toml          # Encrypted local variables store (API Keys)
├── data/
│   └── 3_load/
│       └── weather_mart.parquet  # Optimized production Data Mart asset
├── dashboard/
│   ├── overview.py           # General overview page with geospatial map
│   └── uv_analysis.py        # Solar metrics analysis and Gemini AI integration
├── .gitignore                # Git structural ignore protocol
├── app.py                    # Platform entry point router and navigation controller
└── README.md                 # Project documentation and setup guide

🔒 Security Compliance Note
This repository enforces modern token isolation. No private API authorization headers or infrastructure data layers are hardcoded inside any presentation module. Production deployments utilize official cloud workspace configuration injection parameters to populate st.secrets dynamically.
