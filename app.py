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
                            utils.get_gemini_response(
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
                            utils.get_gemini_response(
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
                            utils.get_gemini_response(
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
                            utils.get_gemini_response(
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
# TAB 2: LIVE AQI (OPTION B ADDED)
# ==================================================
with tab2:
    st.subheader("Live Air Quality Lookup")

    city = st.text_input("Enter city name")

    if st.button("Fetch Live AQI"):
        data = utils.fetch_live_aqi(city)

        if "error" in data:
            st.error(data["error"])
        else:
            # AQI + Category
            st.metric("AQI", data["aqi"])
            st.write(f"**Category:** {data['category']}")

            # ---------- OPTION B: HEALTH ADVISORY (NEW) ----------
            advisory = utils.get_health_advisory(data["aqi"])

            if advisory["alert"]:
                st.error(f"🚨 Air Quality Alert: {advisory['advisory']}")
            else:
                st.info(f"🩺 Health Advisory: {advisory['advisory']}")

            # Pollutant Components
            st.subheader("Pollutant Components (µg/m³)")
            utils.display_components(data["components"])

            # Next 24h / 48h Outlook
            st.subheader("Next 2 Days AQI Outlook")
            st.markdown(
                data["forecast_text"].replace("\n", "  \n")
            )

            # AI Explanation
            st.subheader("AI Explanation")
            with st.spinner("🤖 Generating explanation..."):
                st.write(
                    utils.get_gemini_response(
                        "Explain the current AQI condition, short-term trend, "
                        "health implications, and general precautions.\n\n"
                        f"{data}"
                    )
                )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "AI-generated insights are interpretive and for academic purposes only."
)

