import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
@dataclass
class Config:
    """Конфигурация приложения"""
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    CITY_NAME: str = os.getenv("CITY_NAME", "Krasnoyarsk")
    CITY_ID: int = int(os.getenv("CITY_ID", "1502026"))
    UNITS: str = os.getenv("UNITS", "metric")  # metric = Цельсий
    LANGUAGE: str = os.getenv("LANGUAGE", "ru")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "1800"))  # 30 минут
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    USE_REDIS: bool = os.getenv("USE_REDIS", "false").lower() == "true"


config = Config()
if not config.BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Создай файл .env и добавь токен")
if not config.OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY не задан! Создай файл .env и добавь API ключ")