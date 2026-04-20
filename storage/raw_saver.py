from pathlib import Path
from datetime import datetime, timezone
import json

BASE_DIR = Path(__file__).resolve().parent.parent
base_dir = BASE_DIR / "data" / "raw" / "weather"

def save_raw_payload(city_id: str, payload: dict, base_dir: str = "data/raw/weather") -> str:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    ts_str = now.strftime("%Y-%m-%dT%H-%M-%SZ")

    out_dir = Path(base_dir) / f"city_id={city_id}" / f"date={date_str}"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"{ts_str}.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return str(out_file)