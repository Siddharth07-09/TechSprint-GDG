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
# TAB 1: AQI ANALYSIS
# ==================================================
with tab1:
    file = st.file_uploader("Upload AQI CSV", type=["csv"])

    if file:
        df = utils.load_data(file)

        # ---------- Data Preview ----------
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # ---------- AQI Trend Graph ----------
        st.subheader("AQI Trend Over Time")

        trend_df = (
            df.groupby("Date", as_index=False)["AQI"]
            .mean()
            .sort_values("Date")
        )

        st.line_chart(trend_df.set_index("Date")["AQI"])

        # ---------- AI Summary ----------
        summary = utils.summarize_data(df)

        st.subheader("AI-Powered Insights")

        # SINGLE OUTPUT CONTAINER (already correct)
        output_container = st.container()

        c1, c2, c3, c4 = st.columns(4)

        # ---------- Trend Analysis ----------
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

Present the findings as concise bullet points.
Avoid numeric predictions.

Dataset summary:
{summary}
"""
                            )
                        )

        # ---------- City Comparison ----------
        with c2:
            if st.button("🏙️ City Comparison"):
                with output_container:
                    st.subheader("🏙️ City Comparison Result")
                    with st.spinner("🤖 Comparing air quality across cities..."):
                        st.write(
                            utils.get_gemini_response(
                                f"""
You are conducting a comparative air quality assessment.

Based on the AQI summary below:
- Compare average air quality across cities
- Identify cities with consistently poor air quality
- Highlight relatively cleaner cities

Present findings as bullet points.

Dataset summary:
{summary}
"""
                            )
                        )

        # ---------- Health Impact ----------
        with c3:
            if st.button("🩺 Health Impact"):
                with output_container:
                    st.subheader("🩺 Health Impact Assessment")
                    with st.spinner("🤖 Assessing health implications..."):
                        st.write(
                            utils.get_gemini_response(
                                f"""
You are a public health and environmental risk analyst.

Using the AQI summary below:
- Describe potential health implications
- Identify high-risk population groups
- Suggest general precautionary measures

Present findings as bullet points.

Dataset summary:
{summary}
"""
                            )
                        )

        # ---------- Forecast ----------
        with c4:
            if st.button("🔮 Forecast"):
                with output_container:
                    st.subheader("🔮 AQI Forecast Outlook")
                    with st.spinner("🤖 Generating AQI outlook..."):
                        st.write(
                            utils.get_gemini_response(
                                f"""
You are an air quality forecasting analyst.

Based on historical AQI patterns below, provide a qualitative outlook
for the near future.

Choose exactly ONE:
- IMPROVE
- WORSEN
- STABLE

Justify your choice in 2–3 bullet points.
Do NOT include numeric values.

Dataset summary:
{summary}
"""
                            )
                        )

# ==================================================
# TAB 2: LIVE AQI (UNCHANGED)
# ==================================================
with tab2:
    st.subheader("Live Air Quality Lookup")

    city = st.text_input("Enter city name")

    if st.button("Fetch Live AQI"):
        data = utils.fetch_live_aqi(city)

        if "error" in data:
            st.error(data["error"])
        else:
            st.metric("AQI", data["aqi"])
            st.write(f"**Category:** {data['category']}")

            st.subheader("Pollutant Components (µg/m³)")
            utils.display_components(data["components"])

            st.subheader("Next 2 Days AQI Outlook")
            st.markdown(
                data["forecast_text"].replace("\n", "  \n")
            )

            st.subheader("AI Explanation")
            with st.spinner("🤖 Generating explanation..."):
                st.write(
                    utils.get_gemini_response(
                        "Explain the current AQI condition, "
                        "short-term trend, health implications, "
                        "and general precautions.\n\n"
                        f"{data}"
                    )
                )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "AI-generated insights are interpretive and for academic purposes only."
)

