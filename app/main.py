"""Amazon Best-Selling Books Analysis — Streamlit entrypoint.

Run with: streamlit run app/main.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow running `streamlit run app/main.py` from the repo root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pipeline.analysis import (  # noqa: E402
    genre_distribution,
    price_trend_by_year,
    rating_review_correlation,
    summary_metrics,
    top_authors,
)
from pipeline.clean_data import PROCESSED_DATA_PATH  # noqa: E402
from app.components.charts import (  # noqa: E402
    genre_pie_chart,
    price_trend_line_chart,
    rating_reviews_scatter,
    top_authors_bar_chart,
)
from app.components.filters import apply_filters, render_sidebar_filters  # noqa: E402
from app.utils import fmt_count, fmt_currency, fmt_rating  # noqa: E402

st.set_page_config(page_title="Amazon Best-Selling Books Analysis", layout="wide")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def main() -> None:
    st.title("📚 Amazon Best-Selling Books Analysis")
    st.caption(
        "Exploring the Amazon Top 50 Bestselling Books dataset (2009–2019) "
        "with pandas and an interactive Plotly dashboard."
    )

    with st.spinner("Loading dataset..."):
        try:
            df = load_data(str(PROCESSED_DATA_PATH))
        except FileNotFoundError:
            st.error(
                f"Could not load the dataset. Run `python pipeline/clean_data.py` "
                f"first to generate {PROCESSED_DATA_PATH}."
            )
            st.stop()
        except Exception as exc:  # noqa: BLE001
            st.error(f"Could not load the dataset: {exc}")
            st.stop()

    filters = render_sidebar_filters(df)
    filtered = apply_filters(df, filters)

    metrics = summary_metrics(filtered)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Books", fmt_count(metrics["total_books"]))
    c2.metric("Unique Authors", fmt_count(metrics["unique_authors"]))
    c3.metric("Avg. Price", fmt_currency(metrics["avg_price"]) if metrics["total_books"] else "—")
    c4.metric("Avg. Rating", fmt_rating(metrics["avg_rating"]) if metrics["total_books"] else "—")

    st.divider()

    if filtered.empty:
        st.info("No books match the selected filters — try widening your range.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            genre_pie_chart(genre_distribution(filtered)), use_container_width=True
        )
    with col2:
        st.plotly_chart(
            price_trend_line_chart(price_trend_by_year(filtered)), use_container_width=True
        )

    st.plotly_chart(
        top_authors_bar_chart(top_authors(filtered)), use_container_width=True
    )

    st.subheader("Rating vs. Reviews")
    corr = rating_review_correlation(filtered)
    corr_text = f"{corr:.2f}" if corr == corr else "n/a (not enough data)"
    st.caption(f"Correlation coefficient (rating vs. reviews): {corr_text}")
    st.plotly_chart(rating_reviews_scatter(filtered), use_container_width=True)

    st.subheader("Filtered Data")
    st.dataframe(filtered, use_container_width=True)
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_books.csv",
        mime="text/csv",
    )

    st.divider()
    st.caption(
        f"Data source: Amazon Top 50 Bestselling Books (2009–2019), Kaggle. "
        f"Last updated: {dt.date.today().isoformat()}."
    )


if __name__ == "__main__":
    main()
