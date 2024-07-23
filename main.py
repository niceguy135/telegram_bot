from dotenv import dotenv_values

from utils import BotLogging
from botLogic import bot

ENVS = dotenv_values()

logger = BotLogging.get_logger()


if __name__ == "__main__":
    logger.debug("Bot has been launched!")
    try:
        bot.infinity_polling()
        logger.debug("Bot has closed!")
    except Exception as exc:
        logger.exception(exc)
