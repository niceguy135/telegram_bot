import logging
import datetime
from sys import stdout

from telebot import types

LOG_LEVEL = logging.DEBUG


class BotLogging:

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(stdout)
    formater = logging.Formatter("{%(asctime)s} [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)

    @classmethod
    def get_logger(cls):
        return cls.logger


def log_decor(logger: logging.Logger):
    def actual_log_decor(func_handler):

        def print_simple_log(*args, **kwargs):
            if isinstance(args[0], types.Message):
                logger.debug(f"{func_handler.__name__} has been called! Message: {args[0].text}")
            elif isinstance(args[0], types.CallbackQuery):
                logger.debug(f"{func_handler.__name__} has been called! Callback data: {args[0].data}")
            return func_handler(*args, **kwargs)

        return print_simple_log

    return actual_log_decor


def validate_data(unchecked_data: str) -> tuple[bool, str]:
    """Валидирует дату, приходящую в формате YYYY-MM-DD HH:MM"""

    try:
        v_data, v_time = unchecked_data.split(" ")
    except ValueError:
        return False, "Между датой и временем должен стоять пробел!"

    try:
        datetime.date.fromisoformat(v_data)
    except ValueError:
        return False, "Неправильный формат даты! Должен быть ГГГГ-ММ-ДД"

    try:
        datetime.time.fromisoformat(v_time)
    except ValueError:
        return False, "Неправильный формат времени! Должен быть ЧЧ:ММ"

    return True, ""
