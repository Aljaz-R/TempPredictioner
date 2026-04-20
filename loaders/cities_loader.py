import pandas as pd


def load_active_cities(path: str) -> list[dict]:
    df = pd.read_csv(path)
    df = df[df["is_active"] == 1]
    return df.to_dict(orient="records")