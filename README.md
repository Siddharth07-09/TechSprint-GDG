# 🌤️ AQI Analyst – Air Quality Intelligence Platform (MVP)

## 📌 Overview
**AQI Analyst** is an air-quality intelligence project aimed at helping students, researchers, and local communities understand air pollution patterns through **data-driven analysis and explainable AI**.

The broader vision of this project is to evolve into a **decision-support platform** for air-quality awareness, trend interpretation, and health-risk understanding by combining historical data, real-time environmental information, and AI-based reasoning.

The current implementation is an **MVP**, developed for **TechSprint (GDG on Campus × Hack2skill)**.  
This MVP demonstrates the core idea using Google technologies while remaining realistic, interpretable, and reliable.

---

## 🎯 Problem Statement
Air quality information today is often:
- Fragmented across multiple platforms  
- Difficult for non-experts to interpret  
- Inconsistent or unavailable for many Indian cities  

Many existing systems either show raw AQI numbers without explanation or provide opaque predictions that users cannot easily trust or understand.

---

## 💡 Project Vision
The **AQI Analyst** project aims to:
- Make air-quality data **accessible and interpretable**
- Combine historical trends with real-time conditions
- Use AI to **explain**, not blindly predict
- Support awareness, research, and informed decision-making

---

## ✅ Current Implementation (MVP Features)

### 1️⃣ Historical AQI Analysis (CSV-Based)
- Upload AQI datasets
- Visualize city-wise AQI trends over time
- Compare pollution levels across cities
- Identify seasonal patterns and pollution spikes

### 2️⃣ AI-Powered Insights (Google Gemini)
- Explains AQI trends in plain language
- Provides qualitative city comparisons
- Generates interpretive forecasts:
  - **IMPROVE**
  - **WORSEN**
  - **STABLE**
- Avoids black-box numeric predictions

### 3️⃣ Live Global AQI Lookup (OpenWeatherMap)
- Works for cities worldwide
- Reliable for Indian Tier-2 and Tier-3 cities (e.g., Vijayawada)
- Displays:
  - Current Air Quality Index (OpenWeather scale)
  - Pollutant components (PM2.5, PM10, NO₂, O₃, SO₂, CO)
  - Short-term air-quality trend
- AI explains health implications and general precautions

---

## 🧠 Why Google Gemini?
Google Gemini is used for **reasoning and explanation**, not for raw prediction.

This ensures:
- Transparency  
- Interpretability  
- Ethical and academic correctness  

Gemini analyzes summarized data and produces human-readable insights instead of opaque outputs.

---

## 🌍 Why OpenWeatherMap?
Station-based AQI APIs often lack consistent coverage for many Indian cities.

OpenWeatherMap was chosen because it:
- Uses latitude–longitude based geospatial data  
- Provides global coverage  
- Offers stable and consistent air-pollution data  
- Works reliably for Indian Tier-2 and Tier-3 cities  

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit  
- **Data Processing:** Pandas  
- **AI Reasoning:** Google Gemini (google-genai SDK)  
- **Live AQI Data:** OpenWeatherMap Air Pollution API  
- **Environment Management:** Python dotenv  

---

## 📂 Project Structure
aqi-gemini/

|

├── app.py #Streamlit application

├── utils.py # Core logic (data processing, Gemini, AQI APIs)

├── requirements.txt # Ignored files

├── .gitignore # ignored files

├── README.md # Documentation
