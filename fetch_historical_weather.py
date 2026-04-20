import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from clients.openweather_history_client import fetch_historical_weather
from loaders.cities_loader import load_active_cities


BASE_DIR = Path(__file__).resolve().parent
CITIES_FILE = BASE_DIR / "data" / "metadata" / "cities.csv"
RAW_BASE_DIR = BASE_DIR / "data" / "raw" / "weather_history"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch hourly historical weather data from OpenWeather."
    )
    parser.add_argument(
        "--city",
        type=str,
        default=None,
        help="city_id iz cities.csv, npr. ljubljana",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="zajem za vsa aktivna mesta",
    )
    parser.add_argument(
        "--start",
        type=str,
        required=True,
        help="začetni datum v obliki YYYY-MM-DD",
    )
    parser.add_argument(
        "--end",
        type=str,
        required=True,
        help="končni datum v obliki YYYY-MM-DD",
    )
    return parser.parse_args()


def parse_date_utc(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def iter_hourly_timestamps(start_date: str, end_date: str):
    start_dt = parse_date_utc(start_date)
    end_dt = parse_date_utc(end_date).replace(hour=23, minute=0, second=0)

    current = start_dt
    while current <= end_dt:
        yield current
        current += timedelta(hours=1)


def select_cities(args: argparse.Namespace) -> list[dict]:
    cities = load_active_cities(str(CITIES_FILE))

    if args.city:
        cities = [c for c in cities if c["city_id"] == args.city]
        if not cities:
            raise ValueError(f"Mesto '{args.city}' ne obstaja v {CITIES_FILE}")

    elif not args.all:
        raise ValueError("Podaj --city <city_id> ali --all")

    return cities


def save_historical_raw_payload(city_id: str, request_dt: datetime, payload: dict) -> str:
    date_str = request_dt.strftime("%Y-%m-%d")
    ts_str = request_dt.strftime("%Y-%m-%dT%H-%M-%SZ")

    out_dir = RAW_BASE_DIR / f"city_id={city_id}" / f"date={date_str}"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"{ts_str}.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return str(out_file)


def main() -> None:
    args = parse_args()
    cities = select_cities(args)

    for city in cities:
        print(f"Fetching history for {city['city_name']} ({city['city_id']})")

        for request_dt in iter_hourly_timestamps(args.start, args.end):
            try:
                payload = fetch_historical_weather(
                    lat=float(city["lat"]),
                    lon=float(city["lon"]),
                    dt=request_dt,
                )
                saved_path = save_historical_raw_payload(
                    city_id=city["city_id"],
                    request_dt=request_dt,
                    payload=payload,
                )
                print(
                    f"  OK  {city['city_id']} "
                    f"{request_dt.strftime('%Y-%m-%d %H:%M UTC')} -> {saved_path}"
                )
            except Exception as e:
                print(
                    f"  FAIL {city['city_id']} "
                    f"{request_dt.strftime('%Y-%m-%d %H:%M UTC')} -> {e}"
                )


if __name__ == "__main__":
    main()