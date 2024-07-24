import requests
from pathlib import PurePath
import configparser

from dotenv import dotenv_values

CUR_DIR = PurePath(__file__).parent
WEATHER_TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["WEATHER_TOKEN"]
api_configs = configparser.ConfigParser()
api_configs.read(CUR_DIR.joinpath("apis.ini"))
WEATHER_APIS = api_configs["weatherapi.com"]


class WeatherStatus(str):

    def __init__(self):
        self.result = ""

    def __add__(self, other):
        if isinstance(other, str):
            self.result += other + "\n"
            return self
        else:
            raise TypeError("Add type must be string!")


def get_cur_weather(city: str, aqi=False) -> tuple[bool, dict]:

    res = requests.get(
        url=WEATHER_APIS["CUR_WEATHER_URL"],
        params=[
            ("key", WEATHER_TOKEN),
            ("q", city),
            ("aqi", "no" if aqi is False else "yes")
        ]
    )

    return True if res.ok else False, res.json()


def get_translated_wind_dir(eng_dir: str) -> str:

    result_dir = ""

    for word in eng_dir:
        if word == "N":
            result_dir += "Северо " if len(result_dir) != 1 else "Север"
        elif word == "S":
            result_dir += "Юго " if len(result_dir) != 1 else "Юг"
        elif word == "W":
            result_dir += "Запад"
        elif word == "E":
            result_dir += "Восток"

    return result_dir


def process_json_weather(json: dict) -> str:

    result_status = WeatherStatus()
    cur_weather = json["current"]

    result_status += f"Температура воздуха: {cur_weather['temp_c']} Цельсия"
    result_status += f"Ощущается как {cur_weather['feelslike_c']} Цельсия"
    result_status += f"Скорость ветра: {cur_weather['wind_kph']} км/ч"
    result_status += f"Направление ветра: {get_translated_wind_dir(cur_weather['wind_dir'])}\n"

    pressure = float(cur_weather['pressure_mb']) / 1000 * 750 if cur_weather['pressure_mb'] != "0" else "Неизвестно"
    result_status += f"Давление: {pressure:.1f} мм. рт. ст.\n"

    result_status += f"Влажность: {cur_weather['humidity']}%\n"

    # TODO: подумать на данным куском кода: может есть нечто получше, чем это?
    # не знаю что лучше: match-case или то, что выше. А может вообще есть нечто иное для таких вещей?
    #
    # for weather_property, value in json["current"].items():
    #     match weather_property:
    #         case "temp_c":
    #             result_str += f"Температура воздуха: {value} Цельсия\n"
    #         case "feelslike_c":
    #             result_str += f"Ощущается как {value} Цельсия\n"
    #         case "wind_kph":
    #             result_str += f"Скорость ветра: {value} км/ч\n"
    #         case "wind_dir":
    #             result_str += f"Направление ветра: {get_translated_wind_dir(value)}\n"
    #         case "pressure_mb":
    #             pressure = float(value)/1000*750 if value != "0" else "Неизвестно"
    #             result_str += f"Давление: {pressure} мм. рт. ст.\n"
    #         case "humidity":
    #             result_str += f"Влажность: {value}%\n"

    return result_status.result
