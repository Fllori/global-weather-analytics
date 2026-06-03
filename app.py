import streamlit as st

# ==============================================================================
# GLOBAL PLATFORM CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Weather Pipeline Platform",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# NAVIGATION ARRAIGNMENT & PAGE REGISTRATION
# ==============================================================================
overview_page = st.Page(
    page="dashboard/overview.py", 
    title="General Overview", 
    icon="🌦️"
)

uv_page = st.Page(
    page="dashboard/uv_analysis.py", 
    title="Solar Safety & AI", 
    icon="☀️"
)

# Compile registered pages into the standard native Streamlit navigation sidebar
pipeline_navigation = st.navigation([
    overview_page, 
    uv_page
])

# ==============================================================================
# ROUTER EXECUTION
# ==============================================================================
pipeline_navigation.run()