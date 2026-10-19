"""Stable column names and schema metadata for the bundled dataset."""

from __future__ import annotations

DATASET_COLUMNS = (
    "File",
    "Club",
    "Pitch",
    "Code",
    "Latitude",
    "Longitude",
    "Province",
    "Country",
    "Division",
    "County",
    "Directions",
    "Twitter",
    "Elevation",
    "annual_rainfall",
    "rain_days",
    "Wikipedia",
)

NUMERIC_COLUMNS = ("Latitude", "Longitude", "Elevation", "annual_rainfall", "rain_days")
SEARCH_COLUMNS = ("Club", "Pitch", "County", "Country", "Province")

SCHEMA = {
    "File": ("string", False),
    "Club": ("string", False),
    "Pitch": ("string", False),
    "Code": ("string", True),
    "Latitude": ("number", False),
    "Longitude": ("number", False),
    "Province": ("string", True),
    "Country": ("string", False),
    "Division": ("string", True),
    "County": ("string", True),
    "Directions": ("string", True),
    "Twitter": ("string", True),
    "Elevation": ("number", True),
    "annual_rainfall": ("number", True),
    "rain_days": ("number", True),
    "Wikipedia": ("string", True),
}
