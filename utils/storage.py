from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FILE = DATA_DIR / "predictions.csv"


def save_prediction(record):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if FILE.exists():
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(FILE, index=False)
