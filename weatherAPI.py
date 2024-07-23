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

    return True if res.ok else False, res.json()
