from pathlib import Path

import pandas as pd
import pytest

import gaapitchfinder as gaa


def test_bundled_dataset_loads_with_stable_schema():
    frame = gaa.load_pitches()
    assert len(frame) == 1990
    assert list(frame.columns) == [
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
    ]
    assert frame.attrs["dataset_version"] == "2026.09.19"
    assert pd.api.types.is_float_dtype(frame["Latitude"])


def test_explicit_csv_path(tmp_path: Path):
    source = tmp_path / "pitches.csv"
    source.write_text(
        "Club,Pitch,County,Country,Province,Latitude,Longitude\nA,Ground,,Ireland,Leinster,53,-6\n"
    )
    with pytest.raises(ValueError, match="missing required columns"):
        gaa.load_pitches(source)


def test_search_is_case_insensitive_and_ignores_missing():
    frame = pd.DataFrame(
        {
            "Club": ["Ballymun GAA", pd.NA],
            "Pitch": ["Main", "North"],
            "County": ["Dublin", "Cork"],
            "Country": ["Ireland", "Ireland"],
            "Province": ["Leinster", "Munster"],
        }
    )
    result = gaa.search_pitches("BALLYMUN", frame)
    assert len(result) == 1
    assert result.iloc[0]["Club"] == "Ballymun GAA"


def test_filtering_accepts_lowercase_field_names_and_missing_values():
    frame = gaa.load_pitches()
    dublin = gaa.filter_pitches(county="dublin")
    assert not dublin.empty
    assert dublin["County"].str.casefold().eq("dublin").all()
    missing = gaa.filter_pitches(frame, twitter=None)
    assert missing["Twitter"].isna().all()


def test_nearest_order_and_invalid_coordinates():
    frame = pd.DataFrame(
        {"Club": ["far", "near"], "Latitude": [54.0, 53.35], "Longitude": [-6.0, -6.26]}
    )
    result = gaa.nearest_pitches(53.35, -6.26, limit=2, pitches=frame)
    assert list(result["Club"]) == ["near", "far"]
    assert result.iloc[0]["distance_km"] == pytest.approx(0)
    with pytest.raises(ValueError):
        gaa.nearest_pitches(91, 0, pitches=frame)
    with pytest.raises(ValueError):
        gaa.nearest_pitches(0, 0, limit=0, pitches=frame)


def test_geojson_output_and_missing_coordinates():
    frame = pd.DataFrame(
        {"Club": ["A", "B"], "Latitude": [53.0, pd.NA], "Longitude": [-6.0, pd.NA]}
    )
    geojson = gaa.to_geojson(frame)
    assert geojson["type"] == "FeatureCollection"
    assert geojson["features"][0]["geometry"] == {"type": "Point", "coordinates": [-6.0, 53.0]}
    assert geojson["features"][1]["geometry"] is None


def test_empty_results_and_summaries():
    assert gaa.search_pitches("definitely-not-a-pitch").empty
    assert gaa.filter_pitches(county="definitely-not-a-county").empty
    assert gaa.counts_by_county().sum() == 1990
