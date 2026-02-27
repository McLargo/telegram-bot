"""Python script to be executed when a torrent download is completed."""

#!/usr/bin/python3
import asyncio
import os

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from src.config import Config


async def send_choice():
    """Send a Torrent complete notification to the admin chat.

    In case the notification is triggered by a torrent completion,
    it will include inline keyboard to select the media type (Movie or TV Show)
    for the completed torrent.
    The callback data for the buttons has following format:
    "action|torrent_id|source_path|name"
    Format is knows also by the bot, allowing it to process the user's choice
    when the button is pressed.

    In case of missing environment variables,
    it will send a simple notification without buttons.
    """
    # Load configuration
    config = Config()

    t_id = os.getenv("TR_TORRENT_ID")
    t_dir = os.getenv("TR_TORRENT_DIR")
    t_name = os.getenv("TR_TORRENT_NAME")

    bot = Bot(token=config.token)
    if not all([t_id, t_dir, t_name]):
        config.logger.warning(
            "Missing torrent environment variables, stopping handler.",
        )
        await bot.send_message(
            chat_id=config.admin_chat_id,
            text="📥 *Download Finished!*",
            parse_mode="Markdown",
        )
        return

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎬 Movie",
                    callback_data=f"movies|{t_id}|{t_dir}|{t_name}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📺 TV",
                    callback_data=f"tv_shows|{t_id}|{t_dir}|{t_name}",
                ),
            ],
        ],
    )

    async with bot:
        await bot.send_message(
            chat_id=config.admin_chat_id,
            text=f"📥 *Download Finished*\n{t_name}",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


if __name__ == "__main__":
    asyncio.run(send_choice())
