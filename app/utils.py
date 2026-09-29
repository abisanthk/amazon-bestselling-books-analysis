"""Small display-formatting helpers used by the dashboard."""
from __future__ import annotations


def fmt_currency(value: float) -> str:
    return f"${value:,.2f}"


def fmt_count(value: int) -> str:
    return f"{value:,}"


def fmt_rating(value: float) -> str:
    return f"{value:.2f}"
