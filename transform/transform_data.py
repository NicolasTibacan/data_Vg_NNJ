from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "Name",
    "Platform",
    "Year",
    "Genre",
    "Publisher",
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales",
]


def clean_vgsales(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    cleaned = df.copy()
    cleaned["Publisher"] = cleaned["Publisher"].fillna("Unknown")

    numeric_cols = [
        "Year",
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales",
    ]
    for col in numeric_cols:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned = cleaned.dropna(subset=["Year", "Genre", "Global_Sales"])
    cleaned["Year"] = cleaned["Year"].astype("int64")

    cleaned = cleaned[(cleaned["Year"] >= 1970) & (cleaned["Year"] <= 2025)]
    cleaned = cleaned[cleaned["Global_Sales"] > 0]

    return cleaned.reset_index(drop=True)
