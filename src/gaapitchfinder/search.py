"""Search and field-based filtering helpers."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd

from .data import load_pitches
from .schemas import DATASET_COLUMNS, SEARCH_COLUMNS


def _canonical_field(field: str) -> str:
    fields = {column.casefold(): column for column in DATASET_COLUMNS}
    try:
        return fields[field.casefold()]
    except KeyError as exc:
        raise ValueError(f"Unknown dataset field {field!r}. Valid fields: {', '.join(DATASET_COLUMNS)}") from exc


def search_pitches(query: str, pitches: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return rows containing *query* in any searchable text field.

    Matching is case-insensitive substring matching and ignores missing values.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    frame = load_pitches() if pitches is None else pitches
    mask = pd.Series(False, index=frame.index)
    for column in SEARCH_COLUMNS:
        mask |= frame[column].astype("string").str.contains(query, case=False, regex=False, na=False)
    return frame.loc[mask].reset_index(drop=True)


def filter_pitches(pitches: pd.DataFrame | None = None, **filters: Any) -> pd.DataFrame:
    """Filter rows by named fields using case-insensitive exact text matches.

    A filter value of ``None`` selects missing values. Lists, tuples, and sets
    select any matching value. Unknown field names raise ``ValueError``.
    """
    frame = load_pitches() if pitches is None else pitches
    mask = pd.Series(True, index=frame.index)
    for field, wanted in filters.items():
        field = _canonical_field(field)
        series = frame[field]
        if wanted is None:
            mask &= series.isna()
        elif isinstance(wanted, (list, tuple, set, frozenset)):
            choices = {str(value).casefold() for value in wanted}
            mask &= series.astype("string").str.casefold().isin(choices)
        elif isinstance(wanted, str):
            mask &= series.astype("string").str.casefold().eq(wanted.casefold())
        else:
            mask &= series.eq(wanted)
    return frame.loc[mask].reset_index(drop=True)
