from dataclasses import dataclass
import types

import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

from interfaces import AbstractDatabase


class TodoTask:

    task_data: str
    task_time: str
    description: str


@dataclass
class TodoRecord:

    user_id: int
    user_name: str
    todos: list[TodoTask]


class RedisDatabase(AbstractDatabase):

    def __init__(self, host="localhost", port=6379):

        self.r = redis.Redis(host, port)
        if not self.r.ping():
            raise ConnectionError(f"Cant connect Redis server on {host}:{port}")

    def is_user_exist(self):
        pass

    def init_start_record(self):
        pass

    def create_todo_event(self):
        pass


class AnotherDatabase(AbstractDatabase):

    def is_user_exist(self):
        pass

    def init_start_record(self):
        pass

    def create_todo_event(self):
        pass

def connect_to_db(db_type="redis") -> AbstractDatabase:
    """Фабрика объектов подключенных баз данных"""

    if db_type == "redis":
        return RedisDatabase()
