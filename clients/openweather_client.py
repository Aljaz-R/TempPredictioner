import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_current_weather(lat: float, lon: float, units: str = "metric") -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY ni nastavljen.")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
    }

    response = requests.get(BASE_URL, params=params, timeout=20)

    response.raise_for_status()
    return response.json()