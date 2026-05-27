from config import config
from core.weather_provider import OpenWeatherProvider
from core.cache_service import CacheService
from core.weather_service import WeatherService
from utils.formatters import WeatherFormatter

def test_weather():
    print("Проверка получения погоды...")
    
    
    cache_service = CacheService(use_redis=False)
    
    weather_provider = OpenWeatherProvider(
        api_key=config.OPENWEATHER_API_KEY,
        city_name=config.CITY_NAME,
        city_id=config.CITY_ID,
        units=config.UNITS,
        language=config.LANGUAGE
    )
    
    weather_service = WeatherService(
        provider=weather_provider,
        cache_service=cache_service,
        cache_ttl=1800
    )
    
    
    weather_data = weather_service.get_weather(force_refresh=True)
    
    if weather_data:
        print("\nПогода получена успешно!\n")
        print("=" * 50)
        print(WeatherFormatter.format_current_weather(weather_data))
        print("=" * 50)
        print("\nПрогноз:")
        print(WeatherFormatter.format_forecast(weather_data, days=3))
    else:
        print("\nНе удалось получить погоду!")
        print("Проверь OPENWEATHER_API_KEY в файле .env")

if __name__ == "__main__":
    test_weather()