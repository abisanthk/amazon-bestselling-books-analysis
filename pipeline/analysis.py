"""Pure pandas aggregation functions over the cleaned books dataset.

No Streamlit imports here either — these are unit-tested independently and
called from the dashboard layer in app/.
"""
from __future__ import annotations

import pandas as pd

DEFAULT_TOP_N_AUTHORS = 10


def top_authors(df: pd.DataFrame, n: int = DEFAULT_TOP_N_AUTHORS) -> pd.DataFrame:
    """Return the top `n` authors by number of appearances in the dataset."""
    counts = (
        df["author"]
        .value_counts()
        .head(n)
        .rename_axis("author")
        .reset_index(name="appearances")
    )
    return counts


def genre_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Return genre + count of books in each genre."""
    return (
        df["genre"]
        .value_counts()
        .rename_axis("genre")
        .reset_index(name="count")
    )


def price_trend_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Return year + average price, sorted by year."""
    return (
        df.groupby("year", as_index=False)["price"]
        .mean()
        .rename(columns={"price": "avg_price"})
        .sort_values("year")
        .reset_index(drop=True)
    )


def avg_rating_by_genre(df: pd.DataFrame) -> pd.DataFrame:
    """Return genre + average user rating."""
    return (
        df.groupby("genre", as_index=False, observed=True)["user_rating"]
        .mean()
        .rename(columns={"user_rating": "avg_rating"})
    )


def rating_review_correlation(df: pd.DataFrame) -> float:
    """Pearson correlation coefficient between user_rating and reviews."""
    if len(df) < 2:
        return float("nan")
    return float(df["user_rating"].corr(df["reviews"]))


def summary_metrics(df: pd.DataFrame) -> dict[str, float | int]:
    """Return headline metrics: total_books, unique_authors, avg_price, avg_rating."""
    return {
        "total_books": int(len(df)),
        "unique_authors": int(df["author"].nunique()),
        "avg_price": float(df["price"].mean()) if len(df) else 0.0,
        "avg_rating": float(df["user_rating"].mean()) if len(df) else 0.0,
    }
