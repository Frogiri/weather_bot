import requests
from datetime import datetime
from typing import Optional, List
from loguru import logger
from models.weather import CurrentWeather, DailyForecast, WeatherData

class OpenWeatherProvider:
    """Провайдер погоды OpenWeatherMap"""
    
    def __init__(self, api_key: str, city_name: str, city_id: int, units: str, language: str):
        self.api_key = api_key
        self.city_name = city_name
        self.city_id = city_id
        self.units = units
        self.language = language
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """Выполняет запрос к API"""
        params.update({
            "appid": self.api_key,
            "units": self.units,
            "lang": self.language
        })
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenWeatherMap API error: {e}")
            return None
    
    def get_current_weather(self) -> Optional[CurrentWeather]:
        """Получает текущую погоду"""
        data = self._make_request("weather", {"id": self.city_id})
        if not data:
            return None
        
        return CurrentWeather(
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            wind_direction=data["wind"].get("deg", 0),
            description=data["weather"][0]["description"],
            icon=data["weather"][0]["icon"],
            timestamp=datetime.fromtimestamp(data["dt"])
        )
    
    def get_forecast(self, days: int = 5) -> List[DailyForecast]:
        """Получает прогноз на N дней"""
        data = self._make_request("forecast", {"id": self.city_id})
        if not data:
            return []
        
        # Группируем по дням (API даёт данные каждые 3 часа)
        forecast_by_day = {}
        for item in data["list"]:
            date = datetime.fromtimestamp(item["dt"]).date()
            if date not in forecast_by_day:
                forecast_by_day[date] = []
            forecast_by_day[date].append(item)
        
        # Формируем прогноз
        forecast = []
        for date, items in list(forecast_by_day.items())[:days]:
            temps = [i["main"]["temp"] for i in items]
            forecast.append(DailyForecast(
                date=datetime.combine(date, datetime.min.time()),
                temp_min=min(temps),
                temp_max=max(temps),
                description=items[0]["weather"][0]["description"],
                humidity=items[0]["main"]["humidity"],
                wind_speed=items[0]["wind"]["speed"],
                icon=items[0]["weather"][0]["icon"]
            ))
        
        return forecast
    
    def get_full_weather(self) -> Optional[WeatherData]:
        """Получает полные данные (текущая погода + прогноз)"""
        current = self.get_current_weather()
        if not current:
            return None
        
        forecast = self.get_forecast(5)
        
        return WeatherData(
            city=self.city_name,
            country="RU",
            current=current,
            forecast=forecast,
            last_update=datetime.now()
        )