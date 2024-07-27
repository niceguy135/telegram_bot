import logging

import telebot

from utils import log_decor
from weatherAPI import get_cur_weather, process_json_weather


start_buttons = [
    "Текущая погода"
]


def init_weather_handlers(bot: telebot.TeleBot, logger=logging.Logger(__name__)):

    @bot.message_handler(func=lambda mes: mes.text in ["Текущая погода", "Новый запрос погоды"])
    @log_decor(logger=logger)
    def cur_weather_handler(message):

        res_text = "Введите название города (можно по-русски или по-английски)"
        send_msg = bot.send_message(message.chat.id, res_text)
        bot.register_next_step_handler(send_msg, call_api_weather)

    @log_decor(logger=logger)
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
