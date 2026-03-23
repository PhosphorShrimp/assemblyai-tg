"""Telegram file extraction and download helpers."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from telegram import Message, Update
from telegram.ext import ContextTypes

from app.utils.mime import is_audio_document

logger = logging.getLogger(__name__)


class UnsupportedMessageTypeError(Exception):
    """Raised when an incoming message type is not supported."""


@dataclass(frozen=True)
class IncomingFile:
    """Normalized file metadata extracted from Telegram message."""

    file_id: str
    file_name: str
    file_size: int


def extract_incoming_file(message: Message) -> IncomingFile:
    """Extract file information from voice/audio/document message."""
    if message.voice:
        return IncomingFile(
            file_id=message.voice.file_id,
            file_name=f"voice_{message.voice.file_unique_id}.ogg",
            file_size=message.voice.file_size or 0,
        )

    if message.audio:
        fallback_name = f"audio_{message.audio.file_unique_id}.mp3"
        return IncomingFile(
            file_id=message.audio.file_id,
            file_name=message.audio.file_name or fallback_name,
            file_size=message.audio.file_size or 0,
        )

    if message.document and is_audio_document(message.document.file_name, message.document.mime_type):
        fallback_name = f"document_{message.document.file_unique_id}.bin"
        return IncomingFile(
            file_id=message.document.file_id,
            file_name=message.document.file_name or fallback_name,
            file_size=message.document.file_size or 0,
        )

    raise UnsupportedMessageTypeError("Unsupported incoming Telegram message type")


async def download_telegram_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    incoming: IncomingFile,
    target_dir: Path,
) -> Path:
    """Download a Telegram file to target directory and return local path."""
    if not update.message:
        raise ValueError("Message is required for file download")

    logger.info("Downloading telegram file: %s", incoming.file_name)
    telegram_file = await context.bot.get_file(incoming.file_id)
    local_path = target_dir / incoming.file_name
    await telegram_file.download_to_drive(custom_path=str(local_path))
    return local_path
