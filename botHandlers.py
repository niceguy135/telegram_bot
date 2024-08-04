import logging
from pathlib import PurePath

import telebot

from utils import log_decor, validate_data, convert_date_n_time
from weatherAPI import get_cur_weather, process_json_weather
from todoAPI import connect_to_db

CUR_DIR = PurePath(__file__).parent

start_buttons = [
    "Текущая погода",
    "Личный ежедневник",
]
db = connect_to_db()


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


def init_todo_handlers(bot: telebot.TeleBot, logger=logging.Logger(__name__)):

    @bot.message_handler(func=lambda mes: mes.text in ["Личный ежедневник", "В меню ежедневника"])
    @log_decor(logger=logger)
    def main_todo_handler(message: telebot.types.Message):

        if not db.is_user_exist(message.from_user.id):
            db.init_start_record(message.from_user)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            telebot.types.KeyboardButton("Занести новую запись"),
            telebot.types.KeyboardButton("Узнать о предстоящих событиях")
        )

        with open(CUR_DIR.joinpath("todo.png"), "rb") as photo:
            bot.send_photo(message.chat.id, photo, "Меню Вашего ежедневника", reply_markup=markup)

    @bot.message_handler(func=lambda mes: mes.text in ["Узнать о предстоящих событиях"])
    @log_decor(logger=logger)
    def get_todo_events(message):

        user_events: list[str] = db.get_todo_events(message.from_user.id)
        bot.send_message(message.chat.id, "Ваш список событий:")
        for user_event in user_events:
            bot.send_message(message.chat.id, user_event)
        main_todo_handler(message)

    @bot.message_handler(func=lambda mes: mes.text in ["Занести новую запись"])
    @log_decor(logger=logger)
    def new_todo_handler(message):
        res_text = "Введите дату события (в формате ГГГГ-ММ-ДД ЧЧ:ММ)"
        send_msg = bot.send_message(message.chat.id, res_text)
        bot.register_next_step_handler(send_msg, enter_data)

    def enter_data(message):

        event_data: str = message.text
        result, msg = validate_data(event_data)
        if not result:
            send_msg = bot.send_message(message.chat.id, msg + "\nПопробуйте еще раз!")
            bot.register_next_step_handler(send_msg, enter_data)

        res_text = "Введите описание события"
        send_msg = bot.send_message(message.chat.id, res_text)
        bot.register_next_step_handler(send_msg, enter_description, event_data)

    def enter_description(message: telebot.types.Message, event_data):

        event_desc: str = message.text or "Без описания"
        if not db.create_todo_event(message.from_user.id, *convert_date_n_time(event_desc), event_desc):
            res_text = "Неудалось найти вашу запись в базе данных! Перенаправляю вас в меню..."
            bot.send_message(message.chat.id, res_text)
            main_todo_handler(message)

        res_text = f"Была создана запись на {event_data} --- {event_desc}"
        bot.send_message(message.chat.id, res_text)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            telebot.types.InlineKeyboardButton(
                "В меню ежедневника"
            ),
            telebot.types.InlineKeyboardButton(
                "В меню"
            )
        )
        bot.send_message(message.chat.id, "Куда дальше?", reply_markup=markup)
