from abc import ABC, abstractmethod


class AbstractDatabase(ABC):

    @abstractmethod
    def is_user_exist(self):
        """Проверяет, есть ли записи о пользователе в БД"""

    @abstractmethod
    def init_start_record(self):
        """Создает базовую структуру записей для дальнейшей работы с ними"""
