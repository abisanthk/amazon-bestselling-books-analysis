"""Plotly chart builders. Each function takes a DataFrame and returns a figure."""
from __future__ import annotations

import pandas as pd
import plotly.express as px

# Consistent genre color mapping across every chart
GENRE_COLORS = {"Fiction": "#4C72B0", "Non Fiction": "#DD8452"}


def genre_pie_chart(genre_dist: pd.DataFrame):
    fig = px.pie(
        genre_dist,
        names="genre",
        values="count",
        title="Genre Distribution",
        color="genre",
        color_discrete_map=GENRE_COLORS,
    )
    fig.update_layout(legend_title_text="Genre")
    return fig


def price_trend_line_chart(price_trend: pd.DataFrame):
    fig = px.line(
        price_trend,
        x="year",
        y="avg_price",
        title="Average Price by Year",
        markers=True,
        labels={"year": "Year", "avg_price": "Average Price (USD)"},
    )
    fig.update_yaxes(tickprefix="$")
    return fig


def top_authors_bar_chart(top_authors_df: pd.DataFrame):
    fig = px.bar(
        top_authors_df.sort_values("appearances"),
        x="appearances",
        y="author",
        orientation="h",
        title="Top Authors by Appearances",
        labels={"appearances": "Appearances", "author": "Author"},
    )
    return fig


def rating_reviews_scatter(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="reviews",
        y="user_rating",
        color="genre",
        color_discrete_map=GENRE_COLORS,
        title="Rating vs. Reviews",
        labels={"reviews": "Reviews", "user_rating": "User Rating"},
        hover_data=["name", "author"],
    )
    return fig
