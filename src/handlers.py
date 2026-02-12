"""Handlers for the Telegram bot application."""

import subprocess
import sys
from typing import List

from telegram import Update
from telegram.error import Conflict
from telegram.ext import ContextTypes

from src.config import Config


class Handlers:
    """Handlers for the Telegram bot application."""

    def __init__(self, config: Config):
        """Initialize the Handlers class with the given configuration."""
        self.config = config
        self.logger = config.logger

    def name_list(self) -> List[str]:
        """Return a list of handler names for logging purposes."""
        return ["hello", "reboot"]

    async def hello(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Simple command handler that replies with a greeting message."""
        await update.message.reply_text(
            f"Hello {update.effective_user.first_name}",
        )

    async def reboot(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Command handler to reboot the system where the bot is running."""
        if str(update.effective_user.id) != self.config.admin_chat_id:
            await update.message.reply_text(
                "⛔ Unauthorized request.",
            )
            self.logger.warning(
                "Unauthorized reboot attempt by %s",
                update.effective_user.id,
            )
            return

        await update.message.reply_text("🔄 Reiniciando el sistema...")
        self.logger.warning(
            "System reboot initiated by admin %s",
            update.effective_user.id,
        )
        subprocess.run(["sudo", "reboot"], check=True)  # noqa: S607

    async def error_handler(
        self,
        _update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Log errors and stop on conflict."""
        self.logger.error(
            "Exception while handling an update: %s",
            context.error,
        )

        # if it's a Conflict error, log and stop the application
        if isinstance(context.error, Conflict):
            self.logger.error(
                "Bot token conflict detected! "
                "Another instance of this bot is already running. Stopping...",
            )
            await context.application.stop()
            await context.application.shutdown()
            sys.exit(1)
