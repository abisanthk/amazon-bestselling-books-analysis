import pandas as pd
import pytest

from pipeline.analysis import (
    avg_rating_by_genre,
    genre_distribution,
    price_trend_by_year,
    rating_review_correlation,
    summary_metrics,
    top_authors,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "book_id": [1, 2, 3, 4, 5],
            "name": ["A", "B", "C", "D", "E"],
            "author": ["X", "X", "Y", "Z", "X"],
            "user_rating": [4.0, 4.5, 3.5, 4.8, 4.2],
            "reviews": [100, 200, 150, 300, 250],
            "price": [10.0, 20.0, 30.0, 10.0, 25.0],
            "year": [2015, 2015, 2016, 2016, 2017],
            "genre": ["Fiction", "Fiction", "Non Fiction", "Fiction", "Non Fiction"],
        }
    )


def test_top_authors(sample_df):
    result = top_authors(sample_df, n=2)
    assert result.iloc[0]["author"] == "X"
    assert result.iloc[0]["appearances"] == 3


def test_genre_distribution(sample_df):
    result = genre_distribution(sample_df).set_index("genre")["count"]
    assert result["Fiction"] == 3
    assert result["Non Fiction"] == 2


def test_price_trend_by_year(sample_df):
    result = price_trend_by_year(sample_df).set_index("year")["avg_price"]
    assert result[2015] == pytest.approx(15.0)
    assert result[2016] == pytest.approx(20.0)
    assert result[2017] == pytest.approx(25.0)


def test_avg_rating_by_genre(sample_df):
    result = avg_rating_by_genre(sample_df).set_index("genre")["avg_rating"]
    assert result["Fiction"] == pytest.approx((4.0 + 4.5 + 4.8) / 3)


def test_rating_review_correlation(sample_df):
    corr = rating_review_correlation(sample_df)
    assert -1.0 <= corr <= 1.0


def test_summary_metrics(sample_df):
    metrics = summary_metrics(sample_df)
    assert metrics["total_books"] == 5
    assert metrics["unique_authors"] == 3
    assert metrics["avg_price"] == pytest.approx(19.0)
    assert metrics["avg_rating"] == pytest.approx((4.0 + 4.5 + 3.5 + 4.8 + 4.2) / 5)
