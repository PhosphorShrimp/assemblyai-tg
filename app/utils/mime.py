"""MIME and extension checks for Telegram documents."""

from __future__ import annotations

from pathlib import Path

AUDIO_MIME_PREFIX = "audio/"
AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".ogg",
    ".oga",
    ".opus",
    ".aac",
    ".wma",
    ".aiff",
    ".amr",
}


def is_audio_document(file_name: str | None, mime_type: str | None) -> bool:
    """Check whether a Telegram document appears to contain audio."""
    if mime_type and mime_type.lower().startswith(AUDIO_MIME_PREFIX):
        return True

    if file_name:
        return Path(file_name).suffix.lower() in AUDIO_EXTENSIONS

    return False
