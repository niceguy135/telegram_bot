from pathlib import PurePath

import telebot
from dotenv import dotenv_values

from utils import log_decor, BotLogging
import botHandlers

CUR_DIR = PurePath(__file__).parent
TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["BOT_TOKEN"]
LOGGER = BotLogging.get_logger()


bot = telebot.TeleBot(TOKEN)
botHandlers.init_weather_handlers(bot, LOGGER)


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda mes: mes.text == "В меню")
@log_decor(logger=LOGGER)
def send_menu(message):

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    for but_text in botHandlers.start_buttons:
        markup.add(
            telebot.types.KeyboardButton(but_text)
        )

    with open(CUR_DIR.joinpath("bot.png"), "rb") as photo:
        bot.send_photo(message.chat.id, photo=photo, caption="Чтобы вы хотели узнать?", reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
@log_decor(logger=LOGGER)
def echo_all(message):
    bot.reply_to(message, f"Я не знаю такую команду: {message.text}. Попробуй другую!")
