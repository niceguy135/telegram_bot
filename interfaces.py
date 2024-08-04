from abc import ABC, abstractmethod
from datetime import date, time as dtime

from telebot import types as tg_types


class AbstractDatabase(ABC):

    @abstractmethod
    def is_user_exist(self, user_id: int):
        """Проверяет, есть ли записи о пользователе в БД"""

    @abstractmethod
    def init_start_record(self, user_info: tg_types.User):
        """Создает базовую структуру записей для дальнейшей работы с ними"""

    @abstractmethod
    def create_todo_event(self, user_id: int, event_date: date, event_time: dtime, event_desc: str) -> bool:
        """Создать запись о предстоящем событии"""

    @abstractmethod
    def get_todo_events(self, user_id: int):
        """Получить все записи пользователя из ежедневника"""
