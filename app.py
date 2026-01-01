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
    layout="wide"
)

st.title("🌤️ Spatio-Temporal AQI Analysis & Forecasting (MVP)")
#st.write(
  #  "Upload a CSV file to analyze air quality trends using **Google Gemini**. "
 #   "This is a research-oriented MVP focusing on AI-based reasoning."
#)

# --------------------------------------------------
# Sidebar: Configuration
# --------------------------------------------------
st.sidebar.header("Configuration")

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.sidebar.file_uploader(
    "Upload AQI Dataset (CSV)",
    type=["csv"]
)

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2 = st.tabs(["📊 AQI Analysis (MVP)", "🌍 Live AQI Lookup"])

# ==================================================
# TAB 1: AQI ANALYSIS MVP (UNCHANGED)
# ==================================================
with tab1:
    if uploaded_file is not None:
        try:
            df = utils.load_data(uploaded_file)
            df = df.sort_values("Date")

            st.subheader("1️⃣ Data Preview")
            st.dataframe(df.head())

            c1, c2, c3 = st.columns(3)
            c1.metric("Cities", df["City"].nunique())
            c2.metric("Records", len(df))
            c3.metric(
                "Date Range",
                f"{df['Date'].min().date()} → {df['Date'].max().date()}"
            )

            st.subheader("2️⃣ AQI Trends Visualization")
            chart_data = df.pivot_table(
                index="Date",
                columns="City",
                values="AQI",
                aggfunc="mean"
            )
            st.line_chart(chart_data)

            st.subheader("3️⃣ AI-Powered Insights")

            if not api_key:
                st.warning("⚠️ Enter Gemini API Key in the sidebar.")
            else:
                if "data_summary" not in st.session_state:
                    st.session_state.data_summary = utils.summarize_data(df)

                summary = st.session_state.data_summary
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("📈 Analyze Trends"):
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

                if "trend" in st.session_state:
                    st.markdown("### 📈 Trend Analysis")
                    st.write(st.session_state.trend)

                with col2:
                    if st.button("🏙️ Compare Cities"):
                        prompt = (
                            "Compare AQI across cities in the summary below.\n"
                            "Identify cleaner cities and those with high variability.\n\n"
                            f"{summary}"
                        )
                        st.session_state.compare = utils.get_gemini_response(prompt, api_key)

                if "compare" in st.session_state:
                    st.markdown("### 🏙️ City Comparison")
                    st.write(st.session_state.compare)

                with col3:
                    if st.button("🔮 Forecast AQI"):
                        prompt = (
                            "Based on the AQI trends below, predict the qualitative "
                            "outlook for the next month.\n"
                            "Choose exactly one: IMPROVE, WORSEN, STABLE.\n"
                            "Do not include numeric values.\n\n"
                            f"{summary}"
                        )
                        st.session_state.forecast = utils.get_gemini_response(prompt, api_key)

                if "forecast" in st.session_state:
                    st.markdown("### 🔮 AQI Outlook")
                    st.write(st.session_state.forecast)

        except Exception as e:
            st.error(str(e))
    else:
        st.info("⬅️ Upload a CSV file to begin.")

# ==================================================
# TAB 2: LIVE AQI LOOKUP (OPENWEATHERMAP)
# ==================================================
with tab2:
    st.subheader("🌍 Live AQI Lookup (Global – OpenWeather)")
    st.write(
        "Fetch **current air pollution levels** and **short-term trends** "
        "for any city worldwide using OpenWeatherMap."
    )

    city_name = st.text_input("Enter city name (e.g., Vijayawada, Delhi, London)")

    if st.button("Fetch Live AQI"):
        if not city_name:
            st.warning("Please enter a city name.")
        else:
            with st.spinner("Resolving city location..."):
                location = utils.get_city_coordinates(city_name)

            if "error" in location:
                st.error(location["error"])
            else:
                with st.spinner("Fetching air quality data..."):
                    pollution = utils.fetch_air_pollution(
                        location["lat"], location["lon"]
                    )

                if "error" in pollution:
                    st.error(pollution["error"])
                else:
                    current = pollution["current"]
                    components = current["components"]

                    st.metric(
                        "Air Quality Index (OpenWeather Scale)",
                        current["main"]["aqi"]
                    )
                    aqi_label_map = {
                        1: "Good",
                        2: "Fair",
                        3: "Moderate",
                        4: "Poor",
                        5: "Very Poor"
                    }

                    st.write(f"**Air Quality Category:** {aqi_label_map.get(current['main']['aqi'], 'Unknown')}")


                    st.subheader("Pollutant Components (μg/m³)")
                    st.json(components)

                    st.subheader("Short-Term AQI Trend (Latest Available Data)")
                    st.caption(
                        "ℹ️ Trend is based on OpenWeather forecast data and "
                        "represents general air quality movement, not exact predictions."
                    )
                    st.json(pollution["forecast"])

                    if api_key:
                        with st.spinner("Generating AI explanation..."):
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

                        st.subheader("AI Explanation")
                        st.write(explanation)
                    else:
                        st.info("Add Gemini API key to get AI explanation.")


