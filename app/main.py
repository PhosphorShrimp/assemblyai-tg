"""Application entrypoint for Telegram bot long polling."""

from __future__ import annotations

import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from app.bot.handlers import audio_message_handler, help_handler, start_handler
from app.config import load_settings
from app.logger import setup_logging
from app.services.assemblyai_client import AssemblyAIClient

logger = logging.getLogger(__name__)


def build_application():
    """Build and configure Telegram application instance."""
    settings = load_settings()

    application = ApplicationBuilder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings
    application.bot_data["assembly_client"] = AssemblyAIClient(
        api_key=settings.assemblyai_api_key,
        base_url=settings.assemblyai_base_url,
        poll_interval_seconds=settings.poll_interval_seconds,
    )

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(
        MessageHandler(
            filters.VOICE | filters.AUDIO | filters.Document.ALL,
            audio_message_handler,
        )
    )

    return application


def main() -> None:
    """Run Telegram bot in long polling mode."""
    setup_logging()
    application = build_application()
    logger.info("Starting Telegram bot (long polling)")
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
