# gaapitchfinder

[![PyPI version](https://img.shields.io/pypi/v/gaapitchfinder.svg)](https://pypi.org/project/gaapitchfinder/)
[![Python versions](https://img.shields.io/pypi/pyversions/gaapitchfinder.svg)](https://pypi.org/project/gaapitchfinder/)
[![Tests](https://github.com/ryanmcg2203/gaapitchfinder-python/actions/workflows/tests.yml/badge.svg)](https://github.com/ryanmcg2203/gaapitchfinder-python/actions/workflows/tests.yml)

`gaapitchfinder` is a small, dependency-light Python package for loading and
working with the [GAA Pitch Finder](https://gaapitchfinder.com) open dataset.
It bundles the canonical CSV snapshot, so importing the package never makes a
network request.

The canonical website and source dataset are maintained in the
[GAA Pitch Finder repository](https://github.com/ryanmcg2203/gaapitchfinder).
The published Python package is available on
[PyPI](https://pypi.org/project/gaapitchfinder/).

## Install

```bash
pip install gaapitchfinder
```

For local development, install the test dependencies with
`pip install -e ".[test]"`.

## Examples

```python
import gaapitchfinder as gaa

pitches = gaa.load_pitches()
gaa.search_pitches("Ballymun")
gaa.filter_pitches(county="Dublin")
gaa.nearest_pitches(latitude=53.35, longitude=-6.26, limit=10)
gaa.to_geojson(pitches)
gaa.counts_by_country()
```

Every operation that loads the default snapshot accepts a DataFrame where
appropriate, and `load_pitches("my-pitches.csv")` loads an explicit CSV. Search
is case-insensitive substring matching across `Club`, `Pitch`, `County`,
`Country`, and `Province`. Filters use case-insensitive exact matching; a
`None` filter selects missing values. `nearest_pitches` returns a
`distance_km` column and uses the haversine distance on WGS84 coordinates.

## Public schema

The package preserves the canonical CSV column names:

| Column | Type | Nullable |
| --- | --- | --- |
| `File`, `Club`, `Pitch`, `Country` | string | no |
| `Code`, `Province`, `Division`, `County`, `Directions`, `Twitter`, `Wikipedia` | string | yes |
| `Latitude`, `Longitude` | number (WGS84) | no |
| `Elevation` | number (metres) | yes |
| `annual_rainfall` | number (millimetres) | yes |
| `rain_days` | number | yes |

The bundled dataset is version `2026.09.19`, generated from the 2026-09-19
source snapshot, with schema version `1.0.0`. These identifiers are available
as `gaa.DATASET_VERSION`, `gaa.DATASET_DATE`, `gaa.SCHEMA_VERSION`, and through
`gaa.dataset_metadata()`.

## Attribution and licence

The package code is MIT licensed. The bundled dataset is licensed under the
[Creative Commons Attribution 4.0 International licence (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
Please credit: “Club and pitch location data from GAA Pitch Finder by Ryan
McGuinness: https://gaapitchfinder.com”.

## Development

```bash
pip install -e ".[test]"
pytest
```

For the full maintainer checks:

```bash
pip install -e ".[dev]"
ruff check .
ruff format --check .
python -m build
twine check dist/*
```

Releases are published from version tags through GitHub Actions using PyPI
Trusted Publishing. See `CONTRIBUTING.md` for the release procedure.
