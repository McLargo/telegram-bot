"""Handlers for the Telegram bot application."""

import subprocess
import sys
from typing import List

from telegram import Update
from telegram.error import Conflict
from telegram.ext import ContextTypes

from src.config import Config
from src.decorators import admin_only
from src.kodi import KodiClient


class Handlers:
    """Handlers for the Telegram bot application."""

    def __init__(self, config: Config):
        """Initialize the Handlers class with the given configuration."""
        self.config = config
        self.logger = config.logger
        self.kodi_client = KodiClient(self.config.kodi, self.logger)

    def name_list(self) -> List[str]:
        """Return a list of handler names for logging purposes."""
        return ["hello", "reboot", "movies", "tvshows"]

    async def hello(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Simple command handler that replies with a greeting message."""
        await update.message.reply_text(
            f"Hello {update.effective_user.first_name}",
        )

    @admin_only(action_name="reboot")
    async def reboot(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Command handler to reboot the system where the bot is running."""
        if self.config.debug:
            self.logger.debug("Reboot command skipped")
        else:
            if self.config.can_send_notification:
                await update.message.reply_text(
                    "🔄 System is rebooting... Bot will be back online shortly",
                )
            self.logger.warning(
                "System reboot initiated by admin %s",
                update.effective_user.id,
            )
            subprocess.run(["sudo", "reboot"], check=True)  # noqa: S607

    @admin_only(action_name="get_movies")
    async def get_movies(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Command handler to get the list of movies from Kodi."""
        response = self.kodi_client.get_movies()
        message = f"🎬 *Movies in Kodi* ({len(response)} total)\n\n"
        for movie in response:
            message += f"🎥 *{movie.title}* ({movie.year})\n"

        await update.message.reply_text(
            message,
            parse_mode="Markdown",
        )

    @admin_only(action_name="get_tv_shows")
    async def get_tv_shows(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Command handler to get the list of TV shows from Kodi."""
        response = self.kodi_client.get_tv_shows()
        message = f"📺 *TV Shows in Kodi* ({len(response)} total)\n\n"
        for show in response:
            message += f"🎭 *{show.title}* ({show.year})\n"

            if show.seasons:
                for season in show.seasons:
                    message += (
                        f"   └ Season {season.season_number}: "
                        f"{season.episode_count} episodes\n"
                    )
            else:
                message += "   └ No seasons found\n"
            message += "\n"

        await update.message.reply_text(
            message,
            parse_mode="Markdown",
        )

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
