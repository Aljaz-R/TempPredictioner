from pathlib import Path

from loaders.cities_loader import load_active_cities
from clients.openweather_client import fetch_current_weather
from storage.raw_saver import save_raw_payload
from preprocess_weather import parse_weather_record
from validate_weather import validate_weather_record
from storage.processed_saver import append_processed_record

BASE_DIR = Path(__file__).resolve().parent
CITIES_FILE = BASE_DIR / "data" / "metadata" / "cities.csv"


def main() -> None:
    cities = load_active_cities(str(CITIES_FILE))

    for city in cities:
        try:
            payload = fetch_current_weather(lat=city["lat"], lon=city["lon"])
            raw_path = save_raw_payload(city["city_id"], payload)
            record = parse_weather_record(payload, city)
            validate_weather_record(record)
            append_processed_record(record)

            print(f"Saved raw data for {city['city_name']} -> {raw_path}")
            print(f"Saved processed row for {city['city_name']}")
        except Exception as e:
            print(f"Failed for {city['city_name']}: {e}")


if __name__ == "__main__":
    main()