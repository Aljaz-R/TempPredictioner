from datetime import datetime, timezone


def parse_weather_record(raw_payload: dict, city_metadata: dict) -> dict:
    weather_0 = raw_payload.get("weather", [{}])[0]
    main = raw_payload.get("main", {})
    wind = raw_payload.get("wind", {})
    clouds = raw_payload.get("clouds", {})
    rain = raw_payload.get("rain", {})
    snow = raw_payload.get("snow", {})

    timestamp_unix = raw_payload.get("dt")
    timestamp_utc = None
    if timestamp_unix is not None:
        timestamp_utc = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc).isoformat()

    return {
        "city_id": city_metadata["city_id"],
        "city_name": city_metadata["city_name"],
        "country_code": city_metadata["country_code"],
        "lat": city_metadata["lat"],
        "lon": city_metadata["lon"],
        "timestamp_utc": timestamp_utc,
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "temp_min": main.get("temp_min"),
        "temp_max": main.get("temp_max"),
        "pressure": main.get("pressure"),
        "humidity": main.get("humidity"),
        "sea_level": main.get("sea_level"),
        "grnd_level": main.get("grnd_level"),
        "visibility": raw_payload.get("visibility"),
        "wind_speed": wind.get("speed"),
        "wind_deg": wind.get("deg"),
        "wind_gust": wind.get("gust"),
        "clouds": clouds.get("all"),
        "rain_1h": rain.get("1h", 0.0),
        "snow_1h": snow.get("1h", 0.0),
        "weather_main": weather_0.get("main"),
        "weather_description": weather_0.get("description"),
        "data_source": "openweather_current",
        "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
    }