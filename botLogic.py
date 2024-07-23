from pathlib import PurePath

import telebot
from dotenv import dotenv_values

from utils import log_decor, BotLogging

CUR_DIR = PurePath(__file__).parent
TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["BOT_TOKEN"]
LOGGER = BotLogging.get_logger()


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'hello'])
@log_decor(logger=LOGGER)
def send_welcome(cls, message):
    cls.bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
@log_decor(logger=LOGGER)
def echo_all(message):
    bot.reply_to(message, message.text)
