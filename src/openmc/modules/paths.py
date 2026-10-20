"""Locations for user-specific OpenMC data."""

import os
from pathlib import Path


def data_dir() -> Path:
    """Follow XDG_DATA_HOME, falling back to ~/.local/share/openmc."""
    configured = os.environ.get("XDG_DATA_HOME")
    base = Path(configured) if configured and Path(configured).is_absolute() else Path.home() / ".local/share"
    return base / "openmc"
