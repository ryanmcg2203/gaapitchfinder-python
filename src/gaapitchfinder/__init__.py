"""Python tools for the GAA Pitch Finder dataset."""

from ._version import DATASET_DATE, DATASET_REVISION, DATASET_VERSION, SCHEMA_VERSION, __version__
from .analysis import counts_by, counts_by_county, counts_by_country, counts_by_province
from .data import dataset_metadata, load_pitches
from .geography import nearest_pitches, to_geojson
from .search import filter_pitches, search_pitches

__all__ = [
    "__version__", "DATASET_VERSION", "DATASET_DATE", "DATASET_REVISION", "SCHEMA_VERSION",
    "dataset_metadata", "load_pitches", "search_pitches", "filter_pitches", "nearest_pitches",
    "to_geojson", "counts_by", "counts_by_county", "counts_by_country", "counts_by_province",
]
