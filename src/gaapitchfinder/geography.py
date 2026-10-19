"""Coordinate-based operations and GeoJSON export."""

from __future__ import annotations

import math
from numbers import Real
from typing import Any

import pandas as pd

from .data import load_pitches


def _coordinate(value: Real, name: str, lower: float, upper: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(float(value)):
        raise ValueError(f"{name} must be a finite number")
    result = float(value)
    if not lower <= result <= upper:
        raise ValueError(f"{name} must be between {lower} and {upper}")
    return result


def nearest_pitches(latitude: Real, longitude: Real, limit: int = 10,
                    pitches: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return the nearest geocoded pitches, with ``distance_km`` appended."""
    lat = _coordinate(latitude, "latitude", -90, 90)
    lon = _coordinate(longitude, "longitude", -180, 180)
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")
    frame = load_pitches() if pitches is None else pitches
    work = frame.copy()
    latitudes = pd.to_numeric(work["Latitude"], errors="coerce")
    longitudes = pd.to_numeric(work["Longitude"], errors="coerce")
    valid = latitudes.notna() & longitudes.notna()
    work = work.loc[valid].copy()
    latitudes = latitudes.loc[valid].map(math.radians)
    longitudes = longitudes.loc[valid].map(math.radians)
    lat1, lon1 = math.radians(lat), math.radians(lon)
    dlat = latitudes - lat1
    dlon = longitudes - lon1
    a = (dlat / 2).map(math.sin) ** 2 + latitudes.map(math.cos) * math.cos(lat1) * (dlon / 2).map(math.sin) ** 2
    work["distance_km"] = (a.map(lambda value: 2 * 6371.0088 * math.asin(math.sqrt(value))))
    return work.sort_values("distance_km", kind="mergesort").head(limit).reset_index(drop=True)


def _json_value(value: Any) -> Any:
    if value is None or value is pd.NA:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value.item() if hasattr(value, "item") else value


def to_geojson(pitches: pd.DataFrame) -> dict[str, Any]:
    """Convert a pitch DataFrame to a GeoJSON FeatureCollection.

    Rows with missing coordinates are retained with ``geometry: null`` so
    optional values are not silently discarded.
    """
    features = []
    for _, row in pitches.iterrows():
        latitude = pd.to_numeric(pd.Series([row.get("Latitude")]), errors="coerce").iloc[0]
        longitude = pd.to_numeric(pd.Series([row.get("Longitude")]), errors="coerce").iloc[0]
        geometry = None if pd.isna(latitude) or pd.isna(longitude) else {
            "type": "Point", "coordinates": [float(longitude), float(latitude)]
        }
        properties = {str(column): _json_value(value) for column, value in row.items()}
        features.append({"type": "Feature", "geometry": geometry, "properties": properties})
    return {"type": "FeatureCollection", "features": features}
