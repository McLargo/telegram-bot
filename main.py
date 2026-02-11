"""Main entry point for the Telegram bot application."""

import sys

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from src.callbacks import Callbacks
from src.config import Config
from src.handlers import Handlers

config = Config()
callbacks = Callbacks(config)

config.logger.debug("Starting bot with post init and post stop callbacks")
app = (
    ApplicationBuilder()
    .token(config.token)
    .post_init(callbacks.post_init)
    .post_stop(callbacks.post_stop)
    .build()
)

# Register handlers
handlers = Handlers(config)
config.logger.debug(
    "Loading following command handlers: %s",
    handlers.name_list(),
)
app.add_handler(CommandHandler("hello", handlers.hello))
app.add_handler(CommandHandler("reboot", handlers.reboot))
app.add_error_handler(handlers.error_handler)

# Start the bot
try:
    config.logger.info("Bot is polling for messages")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
except KeyboardInterrupt:
    config.logger.info("Received keyboard interrupt, shutting down gracefully")
    sys.exit(0)
