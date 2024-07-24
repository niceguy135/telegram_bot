import requests
from pathlib import PurePath
import configparser

from dotenv import dotenv_values

CUR_DIR = PurePath(__file__).parent
WEATHER_TOKEN = dotenv_values(CUR_DIR.joinpath(".token"))["WEATHER_TOKEN"]
api_configs = configparser.ConfigParser()
api_configs.read(CUR_DIR.joinpath("apis.ini"))
WEATHER_APIS = api_configs["weatherapi.com"]


def get_cur_weather(city: str, aqi=False) -> tuple[bool, dict]:

    res = requests.get(
        url=WEATHER_APIS["CUR_WEATHER_URL"],
        params=[
            ("key", WEATHER_TOKEN),
            ("q", city),
            ("aqi", "no" if aqi is False else "yes")
        ]
    )

    print(res.request.url)

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

    result_str = ""

    for weather_property, value in json["current"].items():
        match weather_property:
            case "temp_c":
                result_str += f"Температура воздуха: {value} Цельсия\n"
            case "feelslike_c":
                result_str += f"Ощущается как {value} Цельсия\n"
            case "wind_kph":
                result_str += f"Скорость ветра: {value} км/ч\n"
            case "wind_dir":
                result_str += f"Направление ветра: {get_translated_wind_dir(value)}\n"
            case "pressure_mb":
                pressure = float(value)/1000*750 if value != "0" else "Неизвестно"
                result_str += f"Давление: {pressure} мм. рт. ст.\n"
            case "humidity":
                result_str += f"Влажность: {value}%\n"

    return result_str
