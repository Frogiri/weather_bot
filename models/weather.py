from pydantic import BaseModel
from datetime import datetime
from typing import List

class CurrentWeather(BaseModel):
    """Текущая погода"""
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    description: str
    icon: str
    timestamp: datetime
    
    @property
    def temp_celsius(self) -> str:
        return f"{self.temperature:.0f}°C"
    
    @property
    def feels_like_celsius(self) -> str:
        return f"{self.feels_like:.0f}°C"

class DailyForecast(BaseModel):
    """Прогноз на день"""
    date: datetime
    temp_min: float
    temp_max: float
    description: str
    humidity: int
    wind_speed: float
    icon: str
    
    @property
    def temp_range(self) -> str:
        return f"{self.temp_min:.0f}°C / {self.temp_max:.0f}°C"

class WeatherData(BaseModel):
    """Полные данные о погоде"""
    city: str
    country: str
    current: CurrentWeather
    forecast: List[DailyForecast]
    last_update: datetime