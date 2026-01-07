import streamlit as st
import utils
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Spatio-Temporal AQI Analysis & Forecasting",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Spatio-Temporal AQI Analysis & Forecasting")
st.write(
    "Historical AQI analysis and live air quality insights using AI-based reasoning."
)

tab1, tab2 = st.tabs(["📊 AQI Analysis", "🌍 Live AQI"])

# ==================================================
# TAB 1: AQI ANALYSIS (UNCHANGED)
# ==================================================
with tab1:
    file = st.file_uploader("Upload AQI CSV", type=["csv"])

    if file:
        df = utils.load_data(file)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("AQI Trend Over Time")
        trend_df = (
            df.groupby("Date", as_index=False)["AQI"]
            .mean()
            .sort_values("Date")
        )
        st.line_chart(trend_df.set_index("Date")["AQI"])

        summary = utils.summarize_data(df)
        st.subheader("AI-Powered Insights")

        output_container = st.container()
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            if st.button("📈 Trend Analysis"):
                with output_container:
                    st.subheader("📈 Trend Analysis Result")
                    with st.spinner("🤖 Analyzing AQI trends..."):
                        st.write(
                            utils.cached_gemini_response(
                                f"""
You are an environmental data analyst.

Analyze the AQI dataset summary below and identify:
- Long-term AQI trends
- Seasonal or recurring pollution patterns
- Significant pollution spikes or anomalies

Present findings as concise bullet points.

Dataset summary:
{summary}
"""
                            )
                        )

        with c2:
            if st.button("🏙️ City Comparison"):
                with output_container:
                    st.subheader("🏙️ City Comparison Result")
                    with st.spinner("🤖 Comparing cities..."):
                        st.write(
                            utils.cached_gemini_response(
                                f"""
Compare average AQI levels across cities.
Identify cleaner cities and those with consistently poor air quality.

Dataset summary:
{summary}
"""
                            )
                        )

        with c3:
            if st.button("🩺 Health Impact"):
                with output_container:
                    st.subheader("🩺 Health Impact Assessment")
                    with st.spinner("🤖 Assessing health risks..."):
                        st.write(
                            utils.cached_gemini_response(
                                f"""
Explain potential health impacts of observed AQI levels.
Identify vulnerable groups and suggest general precautions.

Dataset summary:
{summary}
"""
                            )
                        )

        with c4:
            if st.button("🔮 Forecast"):
                with output_container:
                    st.subheader("🔮 AQI Forecast Outlook")
                    with st.spinner("🤖 Generating outlook..."):
                        st.write(
                            utils.cached_gemini_response(
                                f"""
Based on historical AQI trends, choose one:
- IMPROVE
- WORSEN
- STABLE

Justify using bullet points. No numeric values.

Dataset summary:
{summary}
"""
                            )
                        )

# ==================================================
# TAB 2: LIVE AQI (FEATURE 1 + FEATURE 2 + AUTOCOMPLETE)
# ==================================================
with tab2:
    st.subheader("Live Air Quality Lookup")

    # ---------- INDIA CITY LIST (SAFE & STATIC) ----------
    INDIA_CITIES = sorted([
        "Ahmedabad", "Amritsar", "Bangalore", "Bhopal", "Bhubaneswar",
        "Chandigarh", "Chennai", "Coimbatore", "Delhi", "Faridabad",
        "Ghaziabad", "Gurgaon", "Hyderabad", "Indore", "Jaipur",
        "Kanpur", "Kochi", "Kolkata", "Lucknow", "Ludhiana",
        "Madurai", "Meerut", "Mumbai", "Nagpur", "Noida",
        "Patna", "Pune", "Raipur", "Surat", "Thane",
        "Trichy", "Udaipur", "Vadodara", "Varanasi", "Vijayawada",
        "Visakhapatnam"
    ])

    # ---------- SESSION STATE ----------
    if "base_city_data" not in st.session_state:
        st.session_state.base_city_data = None
    if "base_city_name" not in st.session_state:
        st.session_state.base_city_name = None

    # ---------- AUTOCOMPLETE CITY SELECTION ----------
    city = st.selectbox(
        "Select a city",
        options=INDIA_CITIES,
        index=None,
        placeholder="Type to search city (e.g. Bangalore, Delhi)"
    )

    # ---------- FETCH BASE CITY ----------
    if st.button("Fetch Live AQI"):
        if not city:
            st.warning("Please select a city.")
        else:
            st.session_state.base_city_data = utils.fetch_live_aqi(city)
            st.session_state.base_city_name = city

    # ---------- DISPLAY BASE CITY ----------
    if st.session_state.base_city_data:
        data = st.session_state.base_city_data

        if "error" in data:
            st.error(data["error"])
        else:
            st.markdown(f"### 📍 {st.session_state.base_city_name}")

            st.metric("AQI", data["aqi"])

            # ---------- COLOR-CODED CATEGORY ----------
            category = data["category"]
            if category == "Good":
                st.success(f"🟢 AQI Category: {category}")
            elif category in ["Fair", "Moderate"]:
                st.warning(f"🟡 AQI Category: {category}")
            elif category == "Poor":
                st.warning(f"🟠 AQI Category: {category}")
            elif category == "Very Poor":
                st.error(f"🔴 AQI Category: {category}")
            else:
                st.info(f"AQI Category: {category}")

            # ---------- HEALTH ADVISORY ----------
            advisory = utils.get_health_advisory(data["aqi"])
            if advisory["alert"]:
                st.error(f"🚨 Air Quality Alert: {advisory['advisory']}")
            else:
                st.info(f"🩺 Health Advisory: {advisory['advisory']}")

            # ---------- POLLUTANTS ----------
            st.subheader("Pollutant Components (µg/m³)")
            utils.display_components(data["components"])

            # ---------- FEATURE 1: WHY AQI IS HIGH ----------
            if data["aqi"] >= 4:
                st.subheader("Primary Contributors to Poor Air Quality")
                with st.spinner("🤖 Analyzing pollution sources..."):
                    why_prompt = f"""
You are an environmental air-quality analyst.

Based ONLY on the pollutant concentrations below, explain
why the current AQI is elevated.

Pollutant data:
{data["components"]}

Instructions:
- Identify dominant pollutants
- Explain causes in simple terms
- Bullet points only
- No numeric values
"""
                    st.write(utils.cached_gemini_response(why_prompt))

            # ---------- FORECAST ----------
            st.subheader("Next 2 Days AQI Outlook")
            st.markdown(data["forecast_text"].replace("\n", "  \n"))
            
                        # ---------- AI EXPLANATION (BUTTON-BASED, QUOTA SAFE) ----------
            st.subheader("AI Explanation")

            if st.button("Generate AI Explanation"):
                with st.spinner("🤖 Generating AI explanation..."):
                    explanation_prompt = f"""
You are an environmental analyst.

Explain the current air quality situation based on:
- AQI category
- Pollutant composition
- Short-term outlook

Guidelines:
- Use simple language
- Focus on health impact and precautions
- Bullet points only
- No numeric values
- No dates

City AQI data:
{data}
"""
                    st.write(
                        utils.cached_gemini_response(explanation_prompt)
                    )


    # ==================================================
    # FEATURE 2: CITY-TO-CITY COMPARISON
    # ==================================================
    st.markdown("---")
    st.subheader("City-to-City AQI Comparison")

    compare_city = st.selectbox(
        "Select another city to compare",
        options=[c for c in INDIA_CITIES if c != st.session_state.base_city_name],
        index=None,
        placeholder="Type to search another city"
    )

    if st.button("Compare Cities"):
        if not st.session_state.base_city_data:
            st.warning("Please fetch AQI for the first city first.")
        elif not compare_city:
            st.warning("Please select a second city.")
        else:
            compare_data = utils.fetch_live_aqi(compare_city)

            if "error" in compare_data:
                st.error(compare_data["error"])
            else:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"### 📍 {st.session_state.base_city_name}")
                    st.metric("AQI", st.session_state.base_city_data["aqi"])
                    st.write(f"Category: {st.session_state.base_city_data['category']}")

                with col2:
                    st.markdown(f"### 📍 {compare_city}")
                    st.metric("AQI", compare_data["aqi"])
                    st.write(f"Category: {compare_data['category']}")

                st.subheader("AI Comparison Insight")
                with st.spinner("🤖 Comparing air quality..."):
                    st.write(
                        utils.cached_gemini_response(
                            f"""
Compare air quality between two Indian cities.

City 1:
{st.session_state.base_city_data}

City 2:
{compare_data}

Instructions:
- Compare severity
- Identify more polluted city
- Bullet points only
- No numeric values
"""
                        )
                    )

