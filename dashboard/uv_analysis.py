from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st
from google import genai
from google.genai import errors

# ==============================================================================
# AI ENGINE CORE CONNECTION ARCHITECTURE (GEMINI)
# ==============================================================================
def generate_ai_lifestyle_suggestions(city, uv_index, temp_max):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        return "🤖 *Error: GEMINI_API_KEY missing from secrets configurations. Please add it to .streamlit/secrets.toml*"

    if not api_key or api_key.startswith("YOUR_") or api_key == "AICI_PUI_CHEIA_TA_GEMINI_AIZASY...":
        return "🤖 *Please configure a valid GEMINI_API_KEY in your deployment secrets token store to activate AI advisory insights.*"

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an intelligent, elite travel concierge and lifestyle weather consultant.
        Analyze the localized daily forecast metrics provided: City: {city}, UV Index: {uv_index} UVI, Max Temp: {temp_max}°C.
        Generate exactly 3 concise, high-value, localized activity recommendations tailored specifically for this city and these specific climate parameters.
        Incorporate smart, relevant emojis and use clean bullet points. Write your entire response clearly in English.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
        
    except errors.APIError as api_err:
        return f"🤖 *AI Engine Network Fault: Failed to retrieve text layers from Gemini infrastructure. Details: {api_err}*"
    except Exception as generic_err:
        return f"🤖 *Operational Concierge Error: Internal failure occurred processing output fields. Details: {generic_err}*"

# ==============================================================================
# RENDER LAYOUT PRESENTATION FRAMEWORK
# ==============================================================================
st.title("☀️ Solar Safety Center & GenAI Vacation Concierge")
st.markdown(
    "Evaluate ultraviolet exposure levels across your destinations, analyze radiation "
    "risk profiles, and generate personalized, AI-driven activity itineraries."
)

# Target the data mart from our Load layer
script_dir = Path(__file__).resolve().parent.parent
consolidated_daily_path = script_dir / "data" / "3_load" / "weather_mart.parquet"

try:
    # Read production Data Mart via DuckDB
    df = duckdb.query(f"SELECT * FROM '{consolidated_daily_path}'").df()
    df = df.sort_values(by="time")

    # ==============================================================================
    # SIDEBAR FILTERS WITH ADVANCED STATE RETENTION
    # ==============================================================================
    st.sidebar.header("🔍 Location Filters")
    
    # --- STEP 1: COUNTRY SELECTOR WITH MEMORY ---
    available_countries = sorted(df["tara_nume"].dropna().unique().tolist())
    
    # Determină indexul din starea salvată la Overview
    country_index = 0
    if "selected_country_state" in st.session_state and st.session_state["selected_country_state"] in available_countries:
        country_index = available_countries.index(st.session_state["selected_country_state"])

    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=available_countries,
        index=country_index,
        key="uv_country_widget"
    )
    # Suprascrie sesiunea în caz că utilizatorul schimbă țara din această pagină
    st.session_state["selected_country_state"] = selected_country

    # --- STEP 2: CITY SELECTOR WITH MEMORY ---
    df_filtered_by_country = df[df["tara_nume"] == selected_country]
    available_cities = sorted(df_filtered_by_country["oras_nume"].dropna().unique().tolist())
    
    # Determină indexul din starea salvată la Overview
    city_index = 0
    if "selected_city_state" in st.session_state and st.session_state["selected_city_state"] in available_cities:
        city_index = available_cities.index(st.session_state["selected_city_state"])

    selected_city = st.sidebar.selectbox(
        "Select City:",
        options=available_cities,
        index=city_index,
        key="uv_city_widget"
    )
    # Suprascrie sesiunea în caz că utilizatorul schimbă orașul din această pagină
    st.session_state["selected_city_state"] = selected_city

    # Final query slice for the active dashboard visuals
    df_filtered = df[(df["tara_nume"] == selected_country) & (df["oras_nume"] == selected_city)].copy()

    # Isolate the current snapshot data tuple (Latest time entry metrics payload)
    latest_record = df_filtered.sort_values(by="time").iloc[-1]
    active_uv = float(latest_record["uv_index_max"])
    active_temp = float(latest_record["temperature_2m_max"])

    # Determine radiation risk levels based on WHO standards
    if active_uv <= 2.99:
        risk_tier = "Low Risk 🟢"
        safety_notice = "Safe conditions. Minimal skin protection required for standard exposure intervals."
    elif active_uv <= 5.99:
        risk_tier = "Moderate Risk 🟡"
        safety_notice = "SPF 15+ sunscreen advised. Seek shaded areas during peak midday hours."
    elif active_uv <= 7.99:
        risk_tier = "High Risk 🟠"
        safety_notice = "Sunscreen application required. Wear protective hats, sunglasses, and clothing garments."
    else:
        risk_tier = "Extreme Danger 🔴"
        safety_notice = "Avoid direct sun exposure. High cellular skin damage velocity window. Apply max SPF defense."

    # ==============================================================================
    # RENDER INTERACTIVE DASHBOARD MATRIX
    # ==============================================================================
    col_layout1, col_layout2 = st.columns([1, 1])

    with col_layout1:
        st.subheader(f"📊 Active Radiation Status for {selected_city}")
        st.metric("Peak Ultraviolet Index", f"{active_uv:.1f} UVI", delta=risk_tier, delta_color="inverse")
        
        st.markdown(f"**Safety Advisory Protocol:** {safety_notice}")
        st.markdown("---")
        
        st.subheader(f"🤖 Gemini Travel Assistant for {selected_city}")
        st.markdown("*Real-time custom activity itineraries built via Generative AI parsing localized climate indexes:*")
        
        with st.spinner("AI is evaluating weather matrices and crafting recommendations..."):
            ai_itinerary_output = generate_ai_lifestyle_suggestions(selected_city, active_uv, active_temp)
            st.markdown(ai_itinerary_output)

    with col_layout2:
        st.subheader("📈 Weekly Projections & Analytical Risk Zones")
        
        chart_data = df_filtered[["time", "uv_index_max"]].copy()
        chart_data.columns = ["Date", "UV Index"]
        chart_data["Date"] = chart_data["Date"].astype(str)

        zones_data = pd.DataFrame([
            {"ymin": 0, "ymax": 3, "Risk Level": "Low", "HexColor": "#00ff66"},
            {"ymin": 3, "ymax": 6, "Risk Level": "Moderate", "HexColor": "#ffea00"},
            {"ymin": 6, "ymax": 8, "Risk Level": "High", "HexColor": "#ff6600"},
            {"ymin": 8, "ymax": 15, "Risk Level": "Extreme", "HexColor": "#ff0055"}
        ])

        import altair as alt
        
        base = alt.Chart(chart_data).encode(
            x=alt.X("Date:T", title="Timeline", axis=alt.Axis(format="%Y-%m-%d", labelAngle=-45))
        )
        
        background_zones = alt.Chart(zones_data).mark_rect(opacity=0.15).encode(
            y=alt.Y("ymin:Q", scale=alt.Scale(domain=[0, 12]), title="UV Index Scale (UVI)"),
            y2="ymax:Q",
            color=alt.Color("HexColor:N", scale=alt.Scale(type="identity"), title="Risk Zones Table")
        )
        
        metric_line = base.mark_line(point=True, color="#1f77b4", strokeWidth=3).encode(
            y=alt.Y("UV Index:Q")
        )
        
        layered_altair_chart = alt.layer(background_zones, metric_line).properties(
            width="container",
            height=380
        ).configure_axis(
            grid=False
        )
        
        st.altair_chart(layered_altair_chart, use_container_width=True)

except Exception as pipeline_err:
    st.error(f"Failed to compile the active Solar analytics dashboard layer: {pipeline_err}")