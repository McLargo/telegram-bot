"""Decorators for the Telegram bot handlers."""

import functools
from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes


def admin_only(action_name: str = "action") -> Callable:
    """Decorator to restrict handler access to admin users only."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
        ) -> None:
            if str(update.effective_user.id) != self.config.admin_chat_id:
                await update.message.reply_text(
                    "⛔ Unauthorized request.",
                )
                self.logger.warning(
                    "Unauthorized %s attempt by %s",
                    action_name,
                    update.effective_user.id,
                )
                return None
            return await func(self, update, context)

        return wrapper

    return decorator
