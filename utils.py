import pandas as pd
import google.genai as genai
import requests
import os

# ==================================================
# CSV DATA HANDLING (UNCHANGED CORE MVP)
# ==================================================

def load_data(file):
    """
    Reads a CSV file into a Pandas DataFrame and validates the structure.
    """
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()

        required_columns = {"Date", "City", "AQI"}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["AQI"] = pd.to_numeric(df["AQI"], errors="coerce")

        df = df.dropna(subset=["Date", "AQI"])
        return df

    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")


def summarize_data(df):
    """
    Generates a compact statistical summary for Gemini analysis.
    """
    start_date = df["Date"].min().strftime("%Y-%m-%d")
    end_date = df["Date"].max().strftime("%Y-%m-%d")
    cities = df["City"].unique().tolist()

    summary = [
        "### DATASET SUMMARY",
        f"Date Range: {start_date} to {end_date}",
        f"Cities Included: {', '.join(cities)}",
        "\n### CITY-WISE STATISTICS",
    ]

    for city in cities:
        city_df = df[df["City"] == city]

        summary.extend([
            f"\nCity: {city}",
            f"- Min AQI: {city_df['AQI'].min():.2f}",
            f"- Max AQI: {city_df['AQI'].max():.2f}",
            f"- Avg AQI: {city_df['AQI'].mean():.2f}",
            "- Monthly Averages:"
        ])

        monthly = city_df.set_index("Date").resample("ME")["AQI"].mean()
        for d, v in monthly.items():
            if pd.notna(v):
                summary.append(f"  {d.strftime('%Y-%m')}: {v:.1f}")

    return "\n".join(summary)


# ==================================================
# GEMINI RESPONSE HANDLER (UPDATED SDK)
# ==================================================

def get_gemini_response(prompt, api_key):
    """
    Sends a prompt to Google Gemini and returns text response.
    """
    try:
        if not api_key:
            return "Error: Gemini API key missing."

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text if response and response.text else "No response."

    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"


# ==================================================
# OPENWEATHERMAP – LIVE AIR QUALITY
# ==================================================

def get_city_coordinates(city_name):
    """
    Converts city name to latitude & longitude using OpenWeather Geocoding API.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OpenWeather API key not found."}

    url = (
        "https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city_name}&limit=1&appid={api_key}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            return {"error": "City not found."}

        return {
            "name": f"{data[0]['name']}, {data[0].get('country', '')}",
            "lat": data[0]["lat"],
            "lon": data[0]["lon"]
        }

    except requests.exceptions.RequestException:
        return {"error": "Failed to fetch city coordinates."}


def fetch_air_pollution(lat, lon):
    """
    Fetches current and short-term air pollution data from OpenWeatherMap.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OpenWeather API key not found."}

    current_url = (
        "http://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )

    forecast_url = (
        "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )

    try:
        current_resp = requests.get(current_url, timeout=10)
        forecast_resp = requests.get(forecast_url, timeout=10)

        current_resp.raise_for_status()
        forecast_resp.raise_for_status()

        current_data = current_resp.json()["list"][0]
        forecast_data = forecast_resp.json()["list"][:3]

        return {
            "current": current_data,
            "forecast": forecast_data
        }

    except requests.exceptions.RequestException:
        return {"error": "Failed to fetch air pollution data."}
