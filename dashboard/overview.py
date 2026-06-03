from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st
import pydeck as pdk

# ==============================================================================
# PAGE HEADER & PLATFORM INTRO
# ==============================================================================
st.title("🌦️ General Overview & Interactive Map")
st.markdown(
    "Visualize real-time weather alerts, geographic distribution of "
    "precipitation, and temperature patterns across the week."
)

# ==============================================================================
# DYNAMIC PATH RESOLUTION FOR WEATHER MART
# ==============================================================================
current_path = Path(__file__).resolve()

# We check different directory depths to find the absolute root path safely
consolidated_daily_path = None
possible_roots = [current_path.parent, current_path.parent.parent, current_path.parent.parent.parent]

for root in possible_roots:
    target_path = root / "data" / "3_load" / "weather_mart.parquet"
    if target_path.exists():
        consolidated_daily_path = target_path
        break

# Fallback if python is executed from a weird relative directory
if not consolidated_daily_path:
    consolidated_daily_path = current_path.parent.parent / "data" / "3_load" / "weather_mart.parquet"

try:
    # 1. Read the production Data Mart asset using DuckDB
    df = duckdb.query(f"SELECT * FROM '{consolidated_daily_path}'").df()
    
    # Clean and explicitly convert columns to float/string to prevent PyDeck crashes
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["temperature_2m_max"] = pd.to_numeric(df["temperature_2m_max"], errors="coerce")
    df["precipitation_sum"] = pd.to_numeric(df["precipitation_sum"], errors="coerce")
    df["oras_nume"] = df["oras_nume"].astype(str)
    df["tara_nume"] = df["tara_nume"].astype(str)
    
    df = df.sort_values(by="time")

    # ==============================================================================
    # SIDEBAR FILTERS WITH ADVANCED STATE RETENTION
    # ==============================================================================
    st.sidebar.header("🔍 Location Filters")
    
    # --- STEP 1: COUNTRY SELECTOR WITH MEMORY ---
    available_countries = sorted(df["tara_nume"].dropna().unique().tolist())
    
    country_index = 0
    if "selected_country_state" in st.session_state and st.session_state["selected_country_state"] in available_countries:
        country_index = available_countries.index(st.session_state["selected_country_state"])

    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=available_countries,
        index=country_index,
        key="ov_country_widget"
    )
    st.session_state["selected_country_state"] = selected_country

    # --- STEP 2: CITY SELECTOR WITH MEMORY ---
    df_filtered_by_country = df[df["tara_nume"] == selected_country]
    available_cities = sorted(df_filtered_by_country["oras_nume"].dropna().unique().tolist())
    
    city_index = 0
    if "selected_city_state" in st.session_state and st.session_state["selected_city_state"] in available_cities:
        city_index = available_cities.index(st.session_state["selected_city_state"])

    selected_city = st.sidebar.selectbox(
        "Select City:",
        options=available_cities,
        index=city_index,
        key="ov_city_widget"
    )
    st.session_state["selected_city_state"] = selected_city

    df_filtered = df[(df["tara_nume"] == selected_country) & (df["oras_nume"] == selected_city)].copy()

    # ==============================================================================
    # ADVANCED PYDECK GEOSPATIAL MAP (OPTIMIZED RADIUS VALUES)
    # ==============================================================================
    st.subheader("🗺️ European Weather Distribution Center")
    st.markdown(
        "*Color Legend: Blue (Cold) ➔ Green (Mild) ➔ Orange (Hot) ➔ Red (Severe Heat).* "
        "**Bubble Size** dynamically represents the volume of estimated precipitation."
    )

    df_latest_map = df.sort_values("time").groupby("oras_nume").last().reset_index()
    df_latest_map["point_radius"] = (df_latest_map["precipitation_sum"] * 0.3) + 3

    def assign_color_profile(temp):
        if pd.isna(temp): return [150, 150, 150, 160]
        if temp <= 10: return [0, 140, 255, 160]
        elif temp <= 22: return [60, 190, 80, 160]
        elif temp <= 32: return [255, 130, 0, 160]
        else: return [230, 0, 40, 160]

    df_latest_map["color_profile"] = df_latest_map["temperature_2m_max"].apply(assign_color_profile)

    st.pydeck_chart(pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        initial_view_state=pdk.ViewState(
            latitude=50.0,
            longitude=15.0,
            zoom=3.4,
            pitch=0, 
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_latest_map,
                get_position="[longitude, latitude]",
                get_color="color_profile",
                get_radius="point_radius",
                radius_units="pixels",
                radius_min_pixels=3,
                radius_max_pixels=14,
                pickable=True,
                auto_highlight=True
            ),
        ],
        tooltip={
            "html": "<b>City:</b> {oras_nume}<br/>"
                    "<b>Country:</b> {tara_nume}<br/>"
                    "<b>Max Temp:</b> {temperature_2m_max}°C<br/>"
                    "<b>Rainfall:</b> {precipitation_sum} mm",
            "style": {"backgroundColor": "rgba(30, 30, 30, 0.9)", "color": "white", "font-family": "Arial", "zIndex": 10000}
        }
    ))

    st.markdown("---")

    # ==============================================================================
    # KPI METRICS INDICATORS
    # ==============================================================================
    st.subheader(f"📊 Active Forecast Metrics for {selected_city}, {selected_country}")
    
    max_forecast_temp = df_filtered["temperature_2m_max"].max()
    min_forecast_temp = df_filtered["temperature_2m_min"].min()
    total_rain_volume = df_filtered["precipitation_sum"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Forecast Temp", f"{max_forecast_temp:.1f} °C")
    col2.metric("Lowest Forecast Temp", f"{min_forecast_temp:.1f} °C")
    col3.metric("Total Cumulative Rainfall", f"{total_rain_volume:.1f} mm")

    st.markdown("#### 🚨 Smart System Advisories")
    alert_triggered = False

    if max_forecast_temp >= 35:
        st.error(f"**Extreme Heat Advisory:** Temperatures are expected to climb to {max_forecast_temp}°C. Hydrate frequently.")
        alert_triggered = True
    elif max_forecast_temp >= 30:
        st.warning(f"**High Temperature Notice:** Warmer weather conditions ahead. Plan outdoor activities carefully.")
        alert_triggered = True

    if total_rain_volume >= 40:
        st.info(f"**Heavy Rainfall Warning:** Expect high precipitation accumulation ({total_rain_volume:.1f} mm) across the week.")
        alert_triggered = True

    if not alert_triggered:
        st.success("**Stable Weather Profile:** No extreme meteorological thresholds detected for this location.")

    # ==============================================================================
    # VISUALIZATIONS & TIME-SERIES CHARTS
    # ==============================================================================
    st.subheader("📈 Temperature Velocity Trends")
    chart_df = df_filtered.set_index("time")[["temperature_2m_max", "temperature_2m_min"]]
    chart_df.columns = ["Max Temperature (°C)", "Min Temperature (°C)"]
    st.line_chart(chart_df)

    # ==============================================================================
    # RAW DATA EXPOSURE & EXPORT UTILITIES
    # ==============================================================================
    with st.expander("🔍 Inspect granular clean tabular rows for this destination"):
        st.dataframe(df_filtered, use_container_width=True)
        
        st.download_button(
            label="📥 Download City Dataset as CSV File",
            data=df_filtered.to_csv(index=False),
            file_name=f"weather_extract_{selected_city}.csv",
            mime="text/csv"
        )

except Exception as pipeline_err:
    st.error(f"Failed to populate presentation UI dashboard. Traceback: {pipeline_err}")
    st.info(f"Attempted to read data from absolute location: {consolidated_daily_path}")