from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR / "data" / "processed" / "weather" / "weather.csv"

def append_processed_record(record: dict, output_path: str = "data/processed/weather/weather.csv") -> None:
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    new_df = pd.DataFrame([record])

    if out_file.exists():
        old_df = pd.read_csv(out_file)
        df = pd.concat([old_df, new_df], ignore_index=True)
        df = df.drop_duplicates(subset=["city_id", "timestamp_utc"], keep="last")
    else:
        df = new_df

    df.to_csv(out_file, index=False)