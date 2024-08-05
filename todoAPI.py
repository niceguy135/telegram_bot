from dataclasses import dataclass
from datetime import date, time as dtime

import redis
from redis.commands.json.path import Path as RedisPath
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from telebot import types as tg_types

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
    _record_sample = {
        "user_id": None,
        "user_name": None,
        "todos": []
    }
    _todo_sample = {
        "data": "2000-01-01",
        "time": "00:00:00",
        "description": ""
    }
    _schema = (
        TextField("$.user_id", as_name="user_id"),
        TextField("$.user_name", as_name="user_name"),
    )
    _ft_name = "todoevents"
    _user_counter: int = None

    def __init__(self, host="localhost", port=6379):

        self.r = redis.Redis(host, port)
        if not self.r.ping():
            raise ConnectionError(f"Cant connect Redis server on {host}:{port}")

        try:
            RedisDatabase._user_counter = int(self.r.get("user:count"))
        except TypeError:
            self.r.set("user:count", 0)
            RedisDatabase._user_counter = 0

        try:
            self.r.ft(self._ft_name).dropindex()
        except redis.exceptions.ResponseError:
            pass

        self.r.ft(self._ft_name).create_index(
            self._schema,
            definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON)
        )

    def __del__(self):
        self.r.set("user:count", RedisDatabase._user_counter)
        self.r.close()

    def is_user_exist(self, user_id: int) -> bool:

        res = self.r.ft(self._ft_name).search(str(user_id))
        return False if res.total == 0 else True

    def init_start_record(self, user_info: tg_types.User):

        record: dict = self._record_sample.copy()
        record["user_id"] = str(user_info.id)
        record["user_name"] = f"{user_info.first_name} {user_info.last_name}"
        self.r.json().set(f"user:{RedisDatabase._user_counter}", RedisPath.root_path(), record)

        RedisDatabase._user_counter += 1
        self.r.set("user:count", RedisDatabase._user_counter)

    def create_todo_event(self, user_id: int, event_date: date, event_time: dtime, event_desc: str) -> bool:

        todo = self._todo_sample.copy()
        search_res = self.r.ft(self._ft_name).search(str(user_id))
        if search_res.total == 0:
            return False
        db_user_id = search_res.docs[0].id

        todo["date"], todo["time"] = event_date.isoformat(), event_time.isoformat()
        todo["description"] = event_desc

        self.r.json().arrinsert(db_user_id, RedisPath.root_path() + "todos", 0, todo)

        return True

    def get_todo_events(self, user_id: int) -> tuple[bool, list]:

        search_res = self.r.ft(self._ft_name).search(str(user_id))
        print(user_id, self._ft_name)
        print(search_res)
        if search_res.total == 0:
            return False, []
        db_user_id = search_res.docs[0].id

        return True, self.r.json().get(db_user_id, ".todos")


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
