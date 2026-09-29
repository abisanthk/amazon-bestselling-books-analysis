import pandas as pd
import pytest

from pipeline.clean_data import (
    add_decade,
    add_price_bucket,
    coerce_types,
    rename_to_snake_case,
    remove_duplicates,
)


@pytest.fixture
def raw_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Name": ["Book A", "Book A", "Book B", "Book C"],
            "Author": ["Author X", "Author X", "Author Y", "Author Z"],
            "User Rating": [4.5, 4.5, "bad", 3.9],
            "Reviews": [100, 100, 200, 300],
            "Price": [9.99, 9.99, 19.99, "oops"],
            "Year": [2015, 2015, 2016, 2017],
            "Genre": ["Fiction", "Fiction", "Non Fiction", "Fiction"],
        }
    )


def test_missing_column_raises_value_error(tmp_path):
    from pipeline.clean_data import load_raw_csv

    bad_csv = tmp_path / "bad.csv"
    pd.DataFrame({"Name": ["x"]}).to_csv(bad_csv, index=False)

    with pytest.raises(ValueError, match="Missing required column"):
        load_raw_csv(bad_csv)


def test_remove_duplicates(raw_df):
    deduped = remove_duplicates(raw_df)
    assert len(deduped) == 3


def test_coerce_types_reports_nan(raw_df):
    coerced, report = coerce_types(raw_df)
    assert report["User Rating"] == 1
    assert report["Price"] == 1
    assert pd.isna(coerced.loc[2, "User Rating"])
    assert pd.isna(coerced.loc[3, "Price"])


def test_price_bucket_thresholds():
    df = pd.DataFrame({"Price": [5.0, 10.0, 20.0, 25.0, 30.0]})
    bucketed = add_price_bucket(df)
    assert list(bucketed["price_bucket"]) == ["Budget", "Mid", "Mid", "Mid", "Premium"]


def test_decade_derivation():
    df = pd.DataFrame({"Year": [2009, 2012, 2019]})
    result = add_decade(df)
    assert list(result["decade"]) == ["2000s", "2010s", "2010s"]


def test_rename_to_snake_case_adds_book_id():
    df = pd.DataFrame(
        {
            "Name": ["Book A"],
            "Author": ["Author X"],
            "User Rating": [4.5],
            "Reviews": [100],
            "Price": [9.99],
            "Year": [2015],
            "Genre": ["Fiction"],
        }
    )
    renamed = rename_to_snake_case(df)
    assert "book_id" in renamed.columns
    assert renamed["book_id"].tolist() == [1]
    assert list(renamed.columns) == [
        "book_id", "name", "author", "user_rating", "reviews", "price", "year", "genre",
    ]
