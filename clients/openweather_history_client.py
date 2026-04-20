import os
from datetime import datetime, timezone
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"


def _to_unix_utc(dt: datetime | int) -> int:
    if isinstance(dt, int):
        return dt

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    return int(dt.timestamp())


def fetch_historical_weather(
    lat: float,
    lon: float,
    dt: datetime | int,
    units: str = "metric",
    lang: str = "en",
) -> dict[str, Any]:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY ni nastavljen.")

    params = {
        "lat": lat,
        "lon": lon,
        "dt": _to_unix_utc(dt),
        "appid": api_key,
        "units": units,
        "lang": lang,
    }

    response = requests.get(BASE_URL, params=params, timeout=30)

    if not response.ok:
        raise RuntimeError(
            f"OpenWeather history request failed: "
            f"status={response.status_code}, body={response.text}"
        )

    return response.json()