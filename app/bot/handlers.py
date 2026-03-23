"""Telegram update handlers."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from telegram import InputFile, Update
from telegram.ext import ContextTypes

from app.bot import messages
from app.config import Settings
from app.services.assemblyai_client import (
    AssemblyAIClient,
    AssemblyAIPollingError,
    AssemblyAIUploadError,
)
from app.services.docx_builder import build_transcript_docx
from app.services.telegram_files import (
    UnsupportedMessageTypeError,
    download_telegram_file,
    extract_incoming_file,
)
from app.services.transcript_formatter import format_transcript_payload
from app.utils.files import cleanup_dir, create_temp_request_dir

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if update.message:
        await update.message.reply_text(messages.WELCOME)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if update.message:
        await update.message.reply_text(messages.HELP)


async def audio_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming audio-capable messages and return DOCX transcript."""
    if not update.message:
        return

    settings: Settings = context.application.bot_data["settings"]
    assembly_client: AssemblyAIClient = context.application.bot_data["assembly_client"]

    try:
        incoming = extract_incoming_file(update.message)
    except UnsupportedMessageTypeError:
        await update.message.reply_text(messages.UNSUPPORTED)
        return

    if incoming.file_size > settings.max_file_size_bytes:
        await update.message.reply_text(messages.TOO_LARGE.format(max_mb=settings.max_file_size_mb))
        return

    request_dir = create_temp_request_dir()
    try:
        await update.message.reply_text(messages.FILE_RECEIVED)

        try:
            audio_path = await download_telegram_file(update, context, incoming, request_dir)
        except Exception:
            logger.exception("Failed to download telegram file")
            await update.message.reply_text(messages.DOWNLOAD_ERROR)
            return

        await update.message.reply_text(messages.AUDIO_SENT)

        try:
            upload_url = await asyncio.to_thread(assembly_client.upload_file, audio_path)
            transcript_id = await asyncio.to_thread(assembly_client.create_transcript, upload_url)
            transcript_payload = await asyncio.to_thread(assembly_client.poll_transcript, transcript_id)
        except AssemblyAIUploadError:
            logger.exception("AssemblyAI upload/create error")
            await update.message.reply_text(messages.UPLOAD_ERROR)
            return
        except AssemblyAIPollingError:
            logger.exception("AssemblyAI polling error")
            await update.message.reply_text(messages.POLLING_ERROR)
            return

        await update.message.reply_text(messages.TRANSCRIPT_READY)

        try:
            transcript = format_transcript_payload(transcript_payload)
            docx_path = request_dir / "transcription.docx"
            await asyncio.to_thread(
                build_transcript_docx,
                docx_path,
                incoming.file_name,
                transcript,
                datetime.now(),
            )
        except Exception:
            logger.exception("DOCX build failed")
            await update.message.reply_text(messages.DOCX_ERROR)
            return

        with docx_path.open("rb") as file_obj:
            await update.message.reply_document(document=InputFile(file_obj, filename="transcription.docx"))
    except Exception:
        logger.exception("Unexpected processing error")
        await update.message.reply_text(messages.GENERIC_ERROR)
    finally:
        cleanup_dir(request_dir)
