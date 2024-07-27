from pathlib import PurePath

import telebot
from dotenv import dotenv_values

from utils import log_decor, BotLogging
from weatherAPI import get_cur_weather, process_json_weather

CUR_DIR = PurePath(__file__).parent
TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["BOT_TOKEN"]
LOGGER = BotLogging.get_logger()


bot = telebot.TeleBot(TOKEN)
start_buttons = [
    "Текущая погода"
]


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda mes: mes.text == "В меню")
@log_decor(logger=LOGGER)
def send_menu(message):

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    for but_text in start_buttons:
        markup.add(
            telebot.types.KeyboardButton(but_text)
        )

    with open(CUR_DIR.joinpath("bot.png"), "rb") as photo:
        bot.send_photo(message.chat.id, photo=photo, caption="Чтобы вы хотели узнать?", reply_markup=markup)


@bot.message_handler(func=lambda mes: mes.text in ["Текущая погода", "Новый запрос погоды"])
@log_decor(logger=LOGGER)
def cur_weather_handler(message):

    res_text = "Введите название города (можно по-русски или по-английски)"
    send_msg = bot.send_message(message.chat.id, res_text)
    bot.register_next_step_handler(send_msg, call_api_weather)


@log_decor(logger=LOGGER)
def call_api_weather(message: telebot.types.Message):

    city = message.text.capitalize()
    res, weather = get_cur_weather(city)
    if not res:
        res_text = f"Что-то пошло не так! Причина: {weather['error']['message']}"
    else:
        res_weather = process_json_weather(weather)
        res_text = f"Вот текущая погода в городе {city}\n" + res_weather

    bot.send_message(message.chat.id, res_text)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.InlineKeyboardButton(
            "Новый запрос погоды"
        ),
        telebot.types.InlineKeyboardButton(
            "В меню"
        )
    )
    bot.send_message(message.chat.id, "Что-то еще?", reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
@log_decor(logger=LOGGER)
def echo_all(message):
    bot.reply_to(message, f"Я не знаю такую команду: {message.text}. Попробуй другую!")
