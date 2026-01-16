import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
)
logger = logging.getLogger("telegram_bot")

# set our logger to INFO or DEBUG based on environment variable
debug_mode = os.getenv("TELEGRAM_BOT_DEBUG", "False").lower() in ("true", "1", "t")
logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
