"""Utility helpers for the diabetes ML project."""

from pathlib import Path


def project_root() -> Path:
    """Return the absolute path to the project root (diabetes-ml-project).

    This assumes this file lives under `<root>/src/utils.py`.
    """
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    """Return the path to the `data` directory."""
    return project_root() / "data"


def raw_data_dir() -> Path:
    """Return the path to the `data/raw` directory."""
    return data_dir() / "raw"


def processed_data_dir() -> Path:
    """Return the path to the `data/processed` directory."""
    return data_dir() / "processed"

