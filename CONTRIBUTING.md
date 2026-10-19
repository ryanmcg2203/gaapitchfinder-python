# Contributing

## Development setup

Use Python 3.10 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the same checks used by CI before opening a pull request:

```bash
pytest
ruff check .
ruff format --check .
python -m build
twine check dist/*
```

## Dataset changes

The CSV in `src/gaapitchfinder/data/gaapitchfinder.csv` is a bundled snapshot
of the canonical GAA Pitch Finder dataset. Keep its column names compatible
with `src/gaapitchfinder/schemas.py` and update the metadata in
`src/gaapitchfinder/_version.py` when the snapshot changes. Include the source
revision, snapshot date, row count, and any schema changes in the pull request.

Do not add network access to package import or data-loading code.

## Pull requests

Keep changes focused, add or update tests for behaviour changes, and include
licensing or attribution updates when changing the bundled dataset.

## Publishing

Configure Trusted Publishing for the `testpypi` and `pypi` GitHub
Environments before releasing. Use the **Publish Python package** workflow's
manual `testpypi` option to rehearse a release. Publish to PyPI only by
creating a version tag that matches `project.version` in `pyproject.toml`, for
example:

```bash
git switch main
git pull --ff-only origin main
git tag v0.1.0
git push origin v0.1.0
```

PyPI releases are immutable. Never reuse an uploaded version number.
