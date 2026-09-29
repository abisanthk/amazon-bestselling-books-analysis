"""Sidebar filter widgets. Returns a plain dict describing the current selection."""
from __future__ import annotations

import pandas as pd
import streamlit as st


def render_sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")

    if st.sidebar.button("Reset filters"):
        for key in ("year_range", "genres", "price_range"):
            st.session_state.pop(key, None)
        st.rerun()

    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    year_range = st.sidebar.slider(
        "Year range",
        min_value=year_min,
        max_value=year_max,
        value=st.session_state.get("year_range", (year_min, year_max)),
        key="year_range",
    )

    genre_options = sorted(df["genre"].unique().tolist())
    genres = st.sidebar.multiselect(
        "Genre",
        options=genre_options,
        default=st.session_state.get("genres", genre_options),
        key="genres",
    )

    price_min, price_max = float(df["price"].min()), float(df["price"].max())
    price_range = st.sidebar.slider(
        "Price range ($)",
        min_value=price_min,
        max_value=price_max,
        value=st.session_state.get("price_range", (price_min, price_max)),
        key="price_range",
    )

    return {"year_range": year_range, "genres": genres, "price_range": price_range}


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    year_lo, year_hi = filters["year_range"]
    price_lo, price_hi = filters["price_range"]
    genres = filters["genres"] or df["genre"].unique().tolist()

    mask = (
        df["year"].between(year_lo, year_hi)
        & df["price"].between(price_lo, price_hi)
        & df["genre"].isin(genres)
    )
    return df.loc[mask].reset_index(drop=True)
