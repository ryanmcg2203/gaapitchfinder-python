"""Dataset loading and bundled snapshot metadata."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from os import PathLike
from typing import Any

import pandas as pd

from ._version import DATASET_DATE, DATASET_REVISION, DATASET_VERSION, SCHEMA_VERSION
from .schemas import DATASET_COLUMNS, NUMERIC_COLUMNS

_BUNDLED_NAME = "gaapitchfinder.csv"


def dataset_metadata() -> dict[str, str]:
    """Return identifiers for the bundled dataset snapshot and schema."""
    return {
        "dataset_version": DATASET_VERSION,
        "dataset_date": DATASET_DATE,
        "dataset_revision": DATASET_REVISION,
        "schema_version": SCHEMA_VERSION,
        "license": "CC BY 4.0",
        "attribution": "GAA Pitch Finder by Ryan McGuinness (https://gaapitchfinder.com)",
    }


def load_pitches(path: str | PathLike[str] | None = None) -> pd.DataFrame:
    """Load pitches from the bundled CSV or an explicitly supplied CSV path.

    Blank CSV values become pandas missing values. Numeric columns are coerced
    to numeric values and all original column names are preserved.
    """
    csv_path: Any = Path(path) if path is not None else files("gaapitchfinder").joinpath("data", _BUNDLED_NAME)
    frame = pd.read_csv(csv_path, na_values=[""], keep_default_na=True)
    missing = [column for column in DATASET_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")
    frame = frame.loc[:, list(DATASET_COLUMNS)]
    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame.attrs.update(dataset_metadata() if path is None else {"source": str(path)})
    return frame
