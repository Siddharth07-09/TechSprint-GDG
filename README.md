# 🌤️ Spatio-Temporal AQI Analysis & Forecasting

An AI-powered web application that transforms raw air quality data into clear, actionable insights using **Google Gemini AI**.  
The platform enables historical AQI analysis, city-wise comparison, health impact assessment, and short-term AQI outlook for cities worldwide.

This project was developed as part of **TechSprint (GDG on Campus)** with a focus on solving real-world environmental and public health challenges using Google technologies.

---

## 🚩 Problem Statement

Air Quality Index (AQI) data is publicly available but often:
- Presented only as raw numbers
- Difficult for non-technical users to interpret
- Lacking health context and future outlook

As a result, individuals and communities struggle to understand pollution risks and make informed decisions.

---

## 💡 Our Solution

We built a **Spatio-Temporal AQI Analysis Platform** that:
- Analyzes historical AQI data
- Interprets patterns using **Google Gemini AI**
- Explains health impacts in simple language
- Compares air quality across cities
- Provides short-term AQI outlook (next 24–48 hours)
- Displays real-time AQI and pollutant components for any city

The goal is to **bridge the gap between environmental data and human understanding**.

---

## ✨ Key Features

### 📊 Historical AQI Analysis
- Upload AQI datasets (CSV format)
- Visualize AQI trends over time
- Identify long-term and seasonal pollution patterns

### 🤖 AI-Powered Insights (Google Gemini)
- Trend analysis
- City-wise comparison
- Health impact explanation
- Qualitative AQI forecast (IMPROVE / WORSEN / STABLE)

### 🏙️ City Comparison
- Compare average AQI levels across multiple cities
- Identify pollution hotspots and cleaner regions

### 🩺 Health Impact Assessment
- Explains potential health risks
- Highlights vulnerable population groups
- Provides general precautionary guidance

### 🌍 Live AQI Lookup (Global)
- Fetch real-time AQI for any city worldwide
- Displays AQI category (Good, Fair, Moderate, Poor, Very Poor)
- Shows pollutant components (PM2.5, PM10, NO₂, O₃, CO, SO₂, etc.)

### 🔮 Short-Term AQI Outlook
- Qualitative AQI outlook for:
  - Next 24 hours
  - Following 24 hours
- Presented in a human-readable format

---

## 🛠️ Google Technologies Used

- **Google Gemini AI**
  - Core intelligence engine for analysis, reasoning, and explanations
- **Gemini API / Google AI Studio**
  - Enables AI integration within the application
- **Google-Cloud-Compatible Architecture**
  - Designed to scale during future development phases

---

## 🧱 System Architecture (High-Level)

1. User uploads AQI data or enters a city name  
2. Data is cleaned and processed using Python  
3. Historical trends and live data are analyzed  
4. Google Gemini AI generates insights and explanations  
5. Results are visualized through an interactive web interface  

---

## 🖥️ Tech Stack

- **Python**
- **Streamlit** – Web application framework
- **Google Gemini AI**
- **OpenWeatherMap Air Pollution API**
- **Pandas** – Data processing
- **GitHub** – Version control
- **Streamlit Cloud** – Deployment

---


## 📂 Project Structure


aqi-gemini/

|

├── app.py #Streamlit application

├── utils.py # Core logic (data processing, Gemini, AQI APIs)

├── requirements.txt # Ignored files

├── .gitignore # ignored files

├── README.md # Documentation


---
## ▶️ How to Run Locally

### 1️⃣ Clone the repository

- git clone https://github.com/your-username/aqi-analysis-project.git

- cd aqi-analysis-project

### 2️⃣ Install dependencies

- pip install -r requirements.txt

### 3️⃣ Set environment variables

- Create a .env file or .streamlit/secrets.toml with:

  GEMINI_API_KEY=your_gemini_api_key

  OPENWEATHER_API_KEY=your_openweather_api_key

### 4️⃣ Run the app

- streamlit run app.py

## 📌 Future Development (Offline Hackathon Scope)

The following enhancements are planned for the offline campus hackathon phase:

### 🚀 Planned Enhancements

- ML-Based AQI Prediction

    - Train machine learning models on historical AQI data

    -  Predict AQI for the next 24–72 hours

- Advanced Health Risk Scoring

  - AQI-based risk levels

   - Group-specific recommendations (children, elderly, sensitive groups)

-  Smart AQI Alerts

   - Automated alerts for high pollution levels

    -  Preventive recommendations

-  Advanced Comparative Dashboard

     - City-wise AQI ranking

      - Visual heatmaps and severity indicators

-  Decision-Support Insights

     - AI-generated recommendations for citizens and authorities

      - Data-backed insights for awareness and planning

## 🎯 Impact & Use Cases

- Raises awareness about air pollution and health risks

- Helps individuals take preventive actions

- Assists researchers and students in environmental analysis

- Can support urban planning and policy discussions

## ⚠️ Disclaimer

AI-generated insights are interpretive and intended for academic and awareness purposes only.
They should not be considered as medical or regulatory advice.

## 👨‍💻 Team & Contribution

Developed as part of TechSprint – GDG on Campus
Focused on AI-driven problem solving using Google technologies.

## ⭐ Conclusion

This project demonstrates how Google Gemini AI can be used beyond chatbots — as a reasoning engine to interpret real-world environmental data and generate meaningful insights.

The MVP establishes a strong foundation, with a clear roadmap toward a full-scale, intelligent AQI monitoring and decision-support system.
