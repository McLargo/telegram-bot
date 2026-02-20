"""Configuration for the Telegram bot application."""

import logging
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class KodiConfig:
    """Configuration class for Kodi integration."""

    def __init__(self):
        """Initialize the KodiConfig class by loading environment variables."""
        self.ip: str = os.getenv("KODI_IP", "localhost")
        self.port: int = int(os.getenv("KODI_PORT", "8080"))
        self.username: Optional[str] = os.getenv("KODI_USERNAME")
        self.password: Optional[str] = os.getenv("KODI_PASSWORD")


class Config:
    """Configuration class for the Telegram bot application."""

    def __init__(self):
        """Initialize the Config class by loading environment variables."""
        self.token: str = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError(
                "No TELEGRAM_BOT_TOKEN found in environment variables",
            )
        self.admin_chat_id: Optional[str] = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
        self.debug: bool = (
            os.getenv("TELEGRAM_BOT_DEBUG", "False").lower() == "true"
        )
        self._logger: Optional[logging.Logger] = None
        self.kodi = KodiConfig()

    @property
    def can_send_notification(self) -> bool:
        """Determine if the bot should send notifications to the admin chat."""
        return self.admin_chat_id is not None and self.debug is False

    @property
    def logger(self) -> logging.Logger:
        """Get the logger instance, creating it if it doesn't exist."""
        if self._logger is None:
            self._logger = logging.getLogger("telegram_bot")
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        return self._logger
