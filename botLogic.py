from pathlib import PurePath

import telebot
from dotenv import dotenv_values

from utils import log_decor, BotLogging
from weatherAPI import get_cur_weather, process_json_weather

CUR_DIR = PurePath(__file__).parent
TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["BOT_TOKEN"]
LOGGER = BotLogging.get_logger()


bot = telebot.TeleBot(TOKEN)
start_buttons = {
    "Текущая погода": "cur_weather"
}


@bot.message_handler(commands=['start'])
@log_decor(logger=LOGGER)
def send_welcome(message):

    markup = telebot.types.InlineKeyboardMarkup()
    buttons = []

    for but_text, value in start_buttons.items():
        buttons.append(
            telebot.types.InlineKeyboardButton(but_text, callback_data=value)
        )

    markup.add(*buttons)
    bot.send_message(message.chat.id, "Чтобы вы хотели узнать?", reply_markup=markup)


@bot.message_handler(commands=['cur_weather'])
@log_decor(logger=LOGGER)
def cur_weather_handler(message):

    res_text = "Введите название города (можно по-русски или по-английски)"
    send_msg = bot.send_message(message.chat.id, res_text)
    bot.register_next_step_handler(send_msg, call_api_weather)


@log_decor(logger=LOGGER)
def call_api_weather(message: telebot.types.Message):

    print(message.text)

    res, weather = get_cur_weather(message.text)
    if not res:
        res_text = f"Что-то пошло не так! Причина: {weather['error']['message']}"
    else:
        res_weather = process_json_weather(weather)
        res_text = f"Вот текущая погода в городе {message.text}\n" + res_weather

    send_msg = bot.send_message(message.chat.id, res_text)


@bot.message_handler(func=lambda msg: True)
@log_decor(logger=LOGGER)
def echo_all(message):
    bot.reply_to(message, f"Я не знаю такую команду: {message.text}. Попробуй другую!")
