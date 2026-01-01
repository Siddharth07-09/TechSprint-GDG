import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import utils

# --------------------------------------------------
# Load environment variables (.env for local testing)
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AQI Analyst MVP",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom CSS for Better UI
# --------------------------------------------------
st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card-like containers */
    .main .block-container {
        padding: 2rem 3rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Title styling */
    h1 {
        color: #1e3a8a;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #4338ca;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3730a3 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        border-radius: 8px 8px 0 0;
        padding: 0 2rem;
        font-weight: 600;
        background-color: #e0e7ff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Card containers for insights */
    .insight-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# Header with Description
# --------------------------------------------------
st.title("🌤️ Spatio-Temporal AQI Analysis & Forecasting")
st.markdown("""
    <div style='background-color: #f0f4ff; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;'>
        <p style='color: #4338ca; margin: 0; font-size: 1.1rem;'>
            🔬 Research-oriented MVP leveraging <strong>Google Gemini AI</strong> for intelligent air quality analysis and forecasting
        </p>
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar: Configuration
# --------------------------------------------------
st.sidebar.markdown("### ⚙️ Configuration")
st.sidebar.markdown("---")

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload AQI Dataset (CSV)",
    type=["csv"],
    help="Upload a CSV file containing AQI data with Date, City, and AQI columns"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='color: #e0e7ff; font-size: 0.85rem; padding: 1rem;'>
        <strong>📌 Quick Guide:</strong><br/>
        1. Enter your API key<br/>
        2. Upload AQI dataset<br/>
        3. Explore insights & forecasts
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2 = st.tabs(["📊 AQI Analysis (MVP)", "🌍 Live AQI Lookup"])

# ==================================================
# TAB 1: AQI ANALYSIS MVP
# ==================================================
with tab1:
    if uploaded_file is not None:
        try:
            df = utils.load_data(uploaded_file)
            df = df.sort_values("Date")

            # Data Preview Section
            st.markdown("### 1️⃣ Data Overview")
            
            # Metrics in columns with better spacing
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🏙️ Cities", df["City"].nunique())
            with col2:
                st.metric("📋 Records", len(df))
            with col3:
                st.metric("📅 Start Date", df['Date'].min().date())
            with col4:
                st.metric("📅 End Date", df['Date'].max().date())
            
            # Expander for data preview
            with st.expander("👁️ View Data Preview", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)

            # Visualization Section
            st.markdown("### 2️⃣ AQI Trends Visualization")
            chart_data = df.pivot_table(
                index="Date",
                columns="City",
                values="AQI",
                aggfunc="mean"
            )
            st.line_chart(chart_data, use_container_width=True, height=400)

            # AI Insights Section
            st.markdown("### 3️⃣ AI-Powered Insights")

            if not api_key:
                st.warning("⚠️ Please enter your Gemini API Key in the sidebar to unlock AI insights.")
            else:
                if "data_summary" not in st.session_state:
                    with st.spinner("🔄 Preparing data summary..."):
                        st.session_state.data_summary = utils.summarize_data(df)

                summary = st.session_state.data_summary
                
                # Action buttons in columns
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("📈 Analyze Trends", use_container_width=True):
                        with st.spinner("🤖 AI is analyzing trends..."):
                            prompt = (
                                "You are an environmental data analyst.\n\n"
                                "Analyze the AQI data summary below and identify:\n"
                                "- Overall trend\n"
                                "- Seasonal patterns\n"
                                "- Major pollution spikes\n\n"
                                "Do not provide numeric predictions.\n\n"
                                f"{summary}"
                            )
                            st.session_state.trend = utils.get_gemini_response(prompt, api_key)

                with col2:
                    if st.button("🏙️ Compare Cities", use_container_width=True):
                        with st.spinner("🤖 AI is comparing cities..."):
                            prompt = (
                                "Compare AQI across cities in the summary below.\n"
                                "Identify cleaner cities and those with high variability.\n\n"
                                f"{summary}"
                            )
                            st.session_state.compare = utils.get_gemini_response(prompt, api_key)

                with col3:
                    if st.button("🔮 Forecast AQI", use_container_width=True):
                        with st.spinner("🤖 AI is generating forecast..."):
                            prompt = (
                                "Based on the AQI trends below, predict the qualitative "
                                "outlook for the next month.\n"
                                "Choose exactly one: IMPROVE, WORSEN, STABLE.\n"
                                "Do not include numeric values.\n\n"
                                f"{summary}"
                            )
                            st.session_state.forecast = utils.get_gemini_response(prompt, api_key)

                # Display insights with styled containers
                if "trend" in st.session_state:
                    st.markdown("""
                        <div class='insight-card'>
                            <h4>📈 Trend Analysis</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.write(st.session_state.trend)

                if "compare" in st.session_state:
                    st.markdown("""
                        <div class='insight-card'>
                            <h4>🏙️ City Comparison</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.write(st.session_state.compare)

                if "forecast" in st.session_state:
                    st.markdown("""
                        <div class='insight-card'>
                            <h4>🔮 AQI Outlook</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.write(st.session_state.forecast)

        except Exception as e:
            st.error(f"❌ Error processing data: {str(e)}")
    else:
        st.info("⬅️ Upload a CSV file from the sidebar to begin analysis.")
        st.markdown("""
            <div style='text-align: center; padding: 3rem;'>
                <h3 style='color: #64748b;'>📊 No data loaded yet</h3>
                <p style='color: #94a3b8;'>Upload your AQI dataset to start exploring insights</p>
            </div>
        """, unsafe_allow_html=True)

# ==================================================
# TAB 2: LIVE AQI LOOKUP (OPENWEATHERMAP)
# ==================================================
with tab2:
    st.markdown("### 🌍 Live AQI Lookup")
    st.markdown("""
        <div style='background-color: #f0f4ff; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
            <p style='color: #4338ca; margin: 0;'>
                Fetch <strong>real-time air pollution data</strong> and short-term trends for any city worldwide using OpenWeatherMap
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    
    with col1:
        city_name = st.text_input("🔍 Enter city name", placeholder="e.g., Vijayawada, Delhi, London, New York")
    
    with col2:
        st.write("")  # Spacer
        fetch_button = st.button("🚀 Fetch Live AQI", use_container_width=True)

    if fetch_button:
        if not city_name:
            st.warning("⚠️ Please enter a city name.")
        else:
            with st.spinner("📍 Resolving city location..."):
                location = utils.get_city_coordinates(city_name)

            if "error" in location:
                st.error(f"❌ {location['error']}")
            else:
                with st.spinner("🌐 Fetching air quality data..."):
                    pollution = utils.fetch_air_pollution(
                        location["lat"], location["lon"]
                    )

                if "error" in pollution:
                    st.error(f"❌ {pollution['error']}")
                else:
                    current = pollution["current"]
                    components = current["components"]

                    # AQI Display
                    aqi_label_map = {
                        1: ("Good", "#10b981"),
                        2: ("Fair", "#84cc16"),
                        3: ("Moderate", "#f59e0b"),
                        4: ("Poor", "#ef4444"),
                        5: ("Very Poor", "#991b1b")
                    }
                    
                    label, color = aqi_label_map.get(current['main']['aqi'], ("Unknown", "#6b7280"))
                    
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, {color}22 0%, {color}44 100%); 
                                    padding: 2rem; border-radius: 12px; text-align: center; margin: 1.5rem 0;
                                    border: 2px solid {color};'>
                            <h2 style='color: {color}; margin: 0;'>AQI: {current['main']['aqi']}</h2>
                            <h3 style='color: {color}; margin: 0.5rem 0 0 0;'>{label}</h3>
                        </div>
                    """, unsafe_allow_html=True)

                    # Pollutant Components
                    st.markdown("#### 🧪 Pollutant Components (μg/m³)")
                    
                    # Display pollutants in a grid
                    cols = st.columns(4)
                    pollutants = [
                        ("CO", components.get("co", "N/A")),
                        ("NO₂", components.get("no2", "N/A")),
                        ("O₃", components.get("o3", "N/A")),
                        ("PM2.5", components.get("pm2_5", "N/A")),
                        ("PM10", components.get("pm10", "N/A")),
                        ("SO₂", components.get("so2", "N/A")),
                    ]
                    
                    for idx, (name, value) in enumerate(pollutants):
                        with cols[idx % 4]:
                            st.metric(name, f"{value}")

                    # Forecast Section
                    with st.expander("📊 View Short-Term Trend Data", expanded=False):
                        st.caption("ℹ️ Based on OpenWeather forecast data")
                        st.json(pollution["forecast"])

                    # AI Explanation
                    if api_key:
                        with st.spinner("🤖 Generating AI explanation..."):
                            prompt = f"""
You are an environmental analyst.

The following data represents current air pollution conditions and
a short-term forecast from a global monitoring service.

Current air pollution data:
{current}

Short-term forecast data:
{pollution['forecast']}

Your task:
- Explain the current air quality condition
- Indicate whether the trend appears to improve or worsen
- Describe possible health implications
- Provide general precautions

Rules:
- Do NOT mention specific calendar dates
- Do NOT invent numeric AQI values
- Use qualitative language only
- Keep the explanation cautious and concise
"""
                            explanation = utils.get_gemini_response(prompt, api_key)

                        st.markdown("""
                            <div class='insight-card'>
                                <h4>🤖 AI Explanation</h4>
                            </div>
                        """, unsafe_allow_html=True)
                        st.write(explanation)
                    else:
                        st.info("💡 Add Gemini API key in the sidebar to get AI-powered explanation.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 1rem;'>
        <p>🌤️ AQI Analyst MVP | Built with Streamlit & Google Gemini AI</p>
    </div>
""", unsafe_allow_html=True)
