def validate_weather_record(record: dict) -> None:
    if not record["city_id"]:
        raise ValueError("city_id manjka")

    if not record["timestamp_utc"]:
        raise ValueError("timestamp_utc manjka")

    temp = record["temperature"]
    if temp is None or temp < -80 or temp > 60:
        raise ValueError(f"temperature izven območja: {temp}")

    humidity = record["humidity"]
    if humidity is None or humidity < 0 or humidity > 100:
        raise ValueError(f"humidity izven območja: {humidity}")

    lat = record["lat"]
    lon = record["lon"]
    if lat < -90 or lat > 90:
        raise ValueError(f"lat izven območja: {lat}")
    if lon < -180 or lon > 180:
        raise ValueError(f"lon izven območja: {lon}")