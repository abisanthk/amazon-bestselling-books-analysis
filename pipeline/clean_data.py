"""Ingestion and cleaning for the Amazon Best-Selling Books dataset.

All functions here are pure pandas — no Streamlit imports — so they can be
unit-tested and reused outside the dashboard.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

# --- Named constants (no magic numbers) -------------------------------
REQUIRED_COLUMNS = ["Name", "Author", "User Rating", "Reviews", "Price", "Year", "Genre"]

BUDGET_MAX = 10.0
MID_MAX = 25.0

PRICE_BUCKET_BUDGET = "Budget"
PRICE_BUCKET_MID = "Mid"
PRICE_BUCKET_PREMIUM = "Premium"

RAW_DATA_PATH = Path("data/raw/amazon_books.csv")
PROCESSED_DATA_PATH = Path("data/processed/books_clean.csv")


def load_raw_csv(path: Path | str = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw CSV and validate that all required columns are present.

    Raises:
        FileNotFoundError: if the CSV does not exist at `path`.
        ValueError: if any required column is missing.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {path}")

    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicated rows, keeping the first occurrence."""
    return df.drop_duplicates(ignore_index=True)


def coerce_types(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Coerce Price and User Rating to numeric, Year to int.

    Returns the coerced DataFrame plus a dict reporting how many rows became
    NaN per coerced column, so bad data is surfaced rather than silently lost.
    """
    df = df.copy()
    nan_report: dict[str, int] = {}

    for col in ["Price", "User Rating"]:
        before_na = df[col].isna().sum()
        df[col] = pd.to_numeric(df[col], errors="coerce")
        after_na = df[col].isna().sum()
        nan_report[col] = int(after_na - before_na)

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    nan_report["Year"] = int(df["Year"].isna().sum())

    return df, nan_report


def drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing any critical field (Price, User Rating, Year, Genre, Name)."""
    critical = ["Name", "User Rating", "Reviews", "Price", "Year", "Genre"]
    return df.dropna(subset=critical).reset_index(drop=True)


def add_price_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """Add a `price_bucket` column: Budget (<$10), Mid ($10-25), Premium (>$25)."""
    df = df.copy()

    def bucket(price: float) -> str:
        if price < BUDGET_MAX:
            return PRICE_BUCKET_BUDGET
        if price <= MID_MAX:
            return PRICE_BUCKET_MID
        return PRICE_BUCKET_PREMIUM

    df["price_bucket"] = df["Price"].apply(bucket).astype("category")
    return df


def add_decade(df: pd.DataFrame) -> pd.DataFrame:
    """Add a `decade` column derived from Year, e.g. 2009 -> '2000s'."""
    df = df.copy()
    df["decade"] = (df["Year"].astype(int) // 10 * 10).astype(str) + "s"
    df["decade"] = df["decade"].astype("category")
    return df


def rename_to_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to snake_case and add a generated `book_id` surrogate key."""
    df = df.rename(
        columns={
            "Name": "name",
            "Author": "author",
            "User Rating": "user_rating",
            "Reviews": "reviews",
            "Price": "price",
            "Year": "year",
            "Genre": "genre",
        }
    )
    df.insert(0, "book_id", range(1, len(df) + 1))
    df["year"] = df["year"].astype(int)
    df["reviews"] = df["reviews"].astype(int)
    df["genre"] = df["genre"].astype("category")
    return df


def clean_pipeline(raw_path: Path | str = RAW_DATA_PATH) -> tuple[pd.DataFrame, dict[str, int]]:
    """Run the full cleaning pipeline end-to-end and return (clean_df, nan_report)."""
    df = load_raw_csv(raw_path)
    df = remove_duplicates(df)
    df, nan_report = coerce_types(df)
    df = drop_incomplete_rows(df)
    df = add_price_bucket(df)
    df = add_decade(df)
    df = rename_to_snake_case(df)
    return df, nan_report


def save_processed(df: pd.DataFrame, path: Path | str = PROCESSED_DATA_PATH) -> None:
    """Write the cleaned DataFrame to the processed data path, creating dirs as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    clean_df, report = clean_pipeline()
    save_processed(clean_df)
    print(f"Cleaned {len(clean_df)} rows -> {PROCESSED_DATA_PATH}")
    for col, n in report.items():
        if n:
            print(f"  {col}: {n} value(s) coerced to NaN")
