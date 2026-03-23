"""Logging utilities for the application."""

from __future__ import annotations

import logging


def setup_logging() -> None:
    """Configure root logger with a production-like format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
