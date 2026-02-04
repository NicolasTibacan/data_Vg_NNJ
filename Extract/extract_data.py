from pathlib import Path

import pandas as pd


def extract_vgsales(csv_path: Path | str = None) -> pd.DataFrame:
    default_path = Path(__file__).resolve().parent / "vgsales.csv"
    path = Path(csv_path) if csv_path else default_path
    return pd.read_csv(path)
