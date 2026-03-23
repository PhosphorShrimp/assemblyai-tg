"""Application configuration loading."""

from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


@dataclass(frozen=True)
class Settings:
    """Runtime configuration values loaded from environment variables."""

    telegram_bot_token: str
    assemblyai_api_key: str
    assemblyai_base_url: str
    max_file_size_mb: int
    poll_interval_seconds: float

    @property
    def max_file_size_bytes(self) -> int:
        """Maximum user-uploaded file size in bytes."""
        return self.max_file_size_mb * 1024 * 1024


def _required_env(name: str) -> str:
    value = getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def load_settings() -> Settings:
    """Load and validate application settings from .env and environment."""
    load_dotenv(dotenv_path=ENV_PATH)
    return Settings(
        telegram_bot_token=_required_env("TELEGRAM_BOT_TOKEN"),
        assemblyai_api_key=_required_env("ASSEMBLYAI_API_KEY"),
        assemblyai_base_url=_required_env("ASSEMBLYAI_BASE_URL").rstrip("/"),
        max_file_size_mb=int(getenv("MAX_FILE_SIZE_MB", "50")),
        poll_interval_seconds=float(getenv("POLL_INTERVAL_SECONDS", "2")),
    )
