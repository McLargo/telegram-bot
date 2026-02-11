"""Callbacks for the Telegram bot application."""

from src.config import Config


class Callbacks:
    """Callbacks for the Telegram bot application."""

    def __init__(self, config: Config):
        """Initialize the Callbacks class with the given configuration."""
        self.config = config
        self.logger = config.logger

    async def post_init(self, application) -> None:
        """Post-initialization callback for the Telegram bot application.

        Callback method that is called after the bot is initialized
        and ready to receive messages.
        It sends a startup notification to the admin chat if configured.
        """
        self.logger.debug("Post-initialization callback triggered")
        if self.config.send_notifications():
            await application.bot.send_message(
                chat_id=self.config.admin_chat_id,
                text="🤖 Bot is now online and ready to accept messages!",
            )
            self.logger.debug(
                "Sent startup notification to chat %s",
                self.config.admin_chat_id,
            )
        self.logger.info("Bot started successfully")

    async def post_stop(self, application) -> None:
        """Post-stop callback for the Telegram bot application.

        Callback method that is called when the bot is stopping
        but before shutdown.
        It sends a shutdown notification to the admin chat if configured.
        """
        self.logger.debug("Post-stop callback triggered")
        if self.config.send_notifications():
            await application.bot.send_message(
                chat_id=self.config.admin_chat_id,
                text="🛑 Bot is shutting down...",
            )
            self.logger.debug(
                "Sent shutdown notification to chat %s",
                self.config.admin_chat_id,
            )
        self.logger.info("Bot has been stopped")
