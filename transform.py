"""Step 2 of the pipeline: turn raw monthly rates into simple features.

Input:  data/raw/eurusd_monthly.csv          (month, eur_usd)
Output: data/processed/eurusd_features.csv   (+ mom_pct, rolling_3m, big_move)
"""
from pathlib import Path

import pandas as pd

IN_FILE = Path("data/raw/eurusd_monthly.csv")
OUT_FILE = Path("data/processed/eurusd_features.csv")
BIG_MOVE_PCT = 2.0  # flag months where EUR/USD moved more than this (in %)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values("month").reset_index(drop=True).copy()
    out["mom_pct"] = (out["eur_usd"].pct_change() * 100).round(2)
    out["rolling_3m"] = out["eur_usd"].rolling(3).mean().round(4)
    out["big_move"] = out["mom_pct"].abs() > BIG_MOVE_PCT
    return out


def main() -> None:
    df = pd.read_csv(IN_FILE)
    out = add_features(df)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_FILE, index=False)

    flagged = out[out["big_move"]]
    print(f"Wrote {len(out)} rows -> {OUT_FILE}")
    print(f"Months with |change| > {BIG_MOVE_PCT}%: {len(flagged)}")
    if not flagged.empty:
        print(flagged[["month", "eur_usd", "mom_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
