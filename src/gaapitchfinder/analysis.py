"""Small summary helpers."""

from __future__ import annotations

import pandas as pd

from .data import load_pitches
from .schemas import DATASET_COLUMNS


def counts_by(field: str, pitches: pd.DataFrame | None = None) -> pd.Series:
    """Count non-missing rows grouped by a dataset field, descending."""
    canonical = {column.casefold(): column for column in DATASET_COLUMNS}.get(field.casefold())
    if canonical is None:
        raise ValueError(f"Unknown dataset field {field!r}")
    frame = load_pitches() if pitches is None else pitches
    return frame[canonical].dropna().value_counts().rename("count")


def counts_by_county(pitches: pd.DataFrame | None = None) -> pd.Series:
    """Return pitch counts by county."""
    return counts_by("County", pitches)


def counts_by_country(pitches: pd.DataFrame | None = None) -> pd.Series:
    """Return pitch counts by country."""
    return counts_by("Country", pitches)


def counts_by_province(pitches: pd.DataFrame | None = None) -> pd.Series:
    """Return pitch counts by province."""
    return counts_by("Province", pitches)
