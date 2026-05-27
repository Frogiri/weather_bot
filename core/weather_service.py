from typing import Optional
from loguru import logger
from models.weather import WeatherData
from core.weather_provider import OpenWeatherProvider
from core.cache_service import CacheService

class WeatherService:
    """Сервис для работы с погодой (кеширование + провайдер)"""
    
    def __init__(self, provider: OpenWeatherProvider, cache_service: CacheService, cache_ttl: int):
        self.provider = provider
        self.cache = cache_service
        self.cache_ttl = cache_ttl
    
    def get_weather(self, force_refresh: bool = False) -> Optional[WeatherData]:
        """Получает погоду (из кеша или от провайдера)"""
        cache_key = "weather_data"
        
        if not force_refresh:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                logger.info("Возвращаю данные из кеша")
                return WeatherData(**cached_data)
        
        logger.info("Запрашиваю свежие данные от провайдера")
        weather_data = self.provider.get_full_weather()
        
        if weather_data:
            self.cache.set(cache_key, weather_data.dict(), self.cache_ttl)
        
        return weather_data
    
    def clear_cache(self):
        """Очищает кеш"""
        self.cache.clear()
        logger.info("Кеш очищен")