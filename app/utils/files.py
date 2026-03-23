"""Helpers for temporary file handling."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path


def create_temp_request_dir() -> Path:
    """Create a unique temporary directory for a single processing request."""
    return Path(tempfile.mkdtemp(prefix="tg-aai-"))


def cleanup_dir(path: Path) -> None:
    """Delete a directory recursively if it exists."""
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
