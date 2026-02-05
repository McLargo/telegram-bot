"""Main entry point for the Telegram bot application."""

import os
import sys

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from callbacks import post_init, post_stop
from handlers import error_handler, hello
from log import logger

token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

logger.debug("Starting bot with post init and post stop callbacks")
app = (
    ApplicationBuilder()
    .token(token)
    .post_init(post_init)
    .post_stop(post_stop)
    .build()
)

# Register handlers
logger.debug("Loading following command handlers: [hello]")
app.add_handler(CommandHandler("hello", hello))
app.add_error_handler(error_handler)

# Start the bot
try:
    logger.info("Bot is polling for messages")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
except KeyboardInterrupt:
    logger.info("Received keyboard interrupt, shutting down gracefully")
    sys.exit(0)
