import httpx
from datetime import datetime
#from loguru import logger

from pathlib import Path

import config


class WeatherGetter:

    def __init__(self, city_name: str) -> None:
        self.city_name = city_name
        self.url = self._format_weather_url() 

    def _format_weather_url(self) -> str: 
        open_weather_url = config.OPENWEATHER_URL
        return open_weather_url.format(city_name=self.city_name)  

    def get_weather_temp(self) -> float:
        data = httpx.get(self.url)
        data_json = data.json()
        temp = data_json['main']['temp']
        return self._parse_temp(temp)

    def _parse_temp(self, kelvin: float) -> float:
        celsius = round(kelvin - 273.15, 2)
        return celsius 


class TextLogger:
   
    def __init__(self, file: Path):
        self._file = file 

    def log_to_file(self, message: str) -> None:
        now = datetime.now()
        
        with open(self._file, "a") as f:
            f.write(f"{now}\n{message}\n")


class WeatherService:

    def __init__(self):
        self.city_name = self._ask_city_name()
        self.weather_api = WeatherGetter(self.city_name) 
        self.logger = TextLogger(Path.cwd() / "log.txt")

    def display_weather(self) -> None:
        temperature = self.weather_api.get_weather_temp()
        message = f"{self.city_name}_{datetime.now()}_{temperature}" 

        print(message)
        self.logger.log_to_file(message)

    def _ask_city_name(self) -> str:
        city_name = input("Enter your city name: ")
        return city_name.lower() 








        
