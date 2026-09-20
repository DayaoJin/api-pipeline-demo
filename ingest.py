"""Step 1 of the pipeline: pull monthly EUR/USD rates from the ECB API.

Output: data/raw/eurusd_monthly.csv  (columns: month, eur_usd)
"""
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

# ECB Data Portal: EXR = exchange rates, M = monthly, USD per 1 EUR, average of period
API_URL = "https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A"
N_MONTHS = 36
OUT_FILE = Path("data/raw/eurusd_monthly.csv")


def fetch(n_months: int = N_MONTHS) -> pd.DataFrame:
    resp = requests.get(
        API_URL,
        params={"lastNObservations": n_months, "format": "csvdata"},
        timeout=30,
    )
    resp.raise_for_status()  # crash loudly if the API fails -> the scheduled run shows red
    raw = pd.read_csv(StringIO(resp.text))
    df = raw[["TIME_PERIOD", "OBS_VALUE"]].rename(
        columns={"TIME_PERIOD": "month", "OBS_VALUE": "eur_usd"}
    )
    return df.sort_values("month").reset_index(drop=True)


def main() -> None:
    df = fetch()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"Saved {len(df)} rows ({df.month.iloc[0]} to {df.month.iloc[-1]}) -> {OUT_FILE}")


if __name__ == "__main__":
    main()
