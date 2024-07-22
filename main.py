from sys import stdout
import logging
from pathlib import PurePath

import telebot
from dotenv import dotenv_values

CUR_DIR = PurePath(__file__).parent
ENVS = dotenv_values()
TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["BOT_TOKEN"]

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
formater = logging.Formatter("{%(asctime)s} [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
handler.setFormatter(formater)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(TOKEN)


def log_decor(func_handler):
    def print_simple_log(*args, **kwargs):
        logger.debug(f"{func_handler.__name__} has been called! Message: {args[0].text}")
        return func_handler(*args, **kwargs)

    return print_simple_log


@bot.message_handler(commands=['start', 'hello'])
@log_decor
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
@log_decor
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    logger.debug("Bot has been launched!")
    try:
        bot.infinity_polling()
        logger.debug("Bot has closed!")
    except Exception as exc:
        logger.exception(exc)
