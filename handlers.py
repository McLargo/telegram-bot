import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.error import Conflict
from telegram.ext import ContextTypes

from log import logger

# load environment variables from .env file
load_dotenv()

# hello handler
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: restrict to specific user
    # if update.effective_user.id != int(os.getenv("TELEGRAM_ADMIN_CHAT_ID")):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and stop on conflict."""
    logger.error(f"Exception while handling an update: {context.error}")

    # if it's a Conflict error, log and stop the application
    if isinstance(context.error, Conflict):
        logger.error("Bot token conflict detected! Another instance of this bot is already running. Stopping...")
        await context.application.stop()
        await context.application.shutdown()
        sys.exit(1)
