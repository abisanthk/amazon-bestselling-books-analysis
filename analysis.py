import pandas as pd

from pipeline.analysis import (
    top_authors,
    genre_distribution,
    price_trend_by_year,
    avg_rating_by_genre,
    rating_review_correlation,
    summary_metrics,
)

# Load cleaned data
df = pd.read_csv("data/processed/books_clean.csv")

print("\n===== SUMMARY METRICS =====")
print(summary_metrics(df))

print("\n===== TOP AUTHORS =====")
print(top_authors(df))

print("\n===== GENRE DISTRIBUTION =====")
print(genre_distribution(df))

print("\n===== PRICE TREND BY YEAR =====")
print(price_trend_by_year(df))

print("\n===== AVERAGE RATING BY GENRE =====")
print(avg_rating_by_genre(df))

print("\n===== RATING-REVIEW CORRELATION =====")
print(rating_review_correlation(df))