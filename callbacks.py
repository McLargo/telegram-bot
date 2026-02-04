import os
from dotenv import load_dotenv

from log import logger

load_dotenv()


async def post_init(application) -> None:
    """
    Callback method that is called after the bot is initialized
    and ready to receive messages.

    It sends a startup notification to the admin chat if configured.
    """
    logger.debug("Post-initialization callback triggered")
    chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
    if chat_id:
        await application.bot.send_message(
            chat_id=chat_id,
            text="🤖 Bot is now online and ready to accept messages!"
        )
        logger.debug(f"Sent startup notification to chat {chat_id}")
    logger.info("Bot started successfully")


async def post_stop(application) -> None:
    """
    Callback method that is called when the bot is stopping but before shutdown.

    It sends a shutdown notification to the admin chat if configured.
    """
    logger.debug("Post-stop callback triggered")
    chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
    if chat_id:
        await application.bot.send_message(
            chat_id=chat_id,
            text="🛑 Bot is shutting down..."
        )
        logger.debug(f"Sent shutdown notification to chat {chat_id}")
    logger.info("Bot has been stopped")
