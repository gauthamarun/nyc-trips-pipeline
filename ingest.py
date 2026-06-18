# ingest.py
import requests
import pandas as pd
from pathlib import Path

DATASET_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
RAW_DIR = Path(__file__).resolve().parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_data(url: str, dest: Path) -> Path:
    out = dest / url.split("/")[-1]
    if not out.exists():
        print(f"Downloading {url}...")
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with out.open("wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
    return out


if __name__ == "__main__":
    path = download_data(DATASET_URL, RAW_DIR)
    df = pd.read_parquet(path)
    print(df.dtypes)
    print(df.head())
