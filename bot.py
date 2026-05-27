import telebot
from loguru import logger
from config import config
from core.weather_provider import OpenWeatherProvider
from core.cache_service import CacheService
from core.weather_service import WeatherService
from handlers.weather_handlers import WeatherHandlers

logger.add("logs/bot.log", rotation="1 day", retention="7 days", level="INFO")

def main():
    """Точка входа в приложение"""
    
    logger.info("Запуск Weather Bot...")
    
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN не задан в .env файле")
        return
    
    if not config.OPENWEATHER_API_KEY:
        logger.error("OPENWEATHER_API_KEY не задан в .env файле")
        return
    
    cache_service = CacheService(use_redis=config.USE_REDIS)
    
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
        cache_ttl=config.CACHE_TTL
    )
    bot = telebot.TeleBot(config.BOT_TOKEN)
    
    @bot.message_handler(commands=["start", "help"])
    def send_welcome(message):
        bot.reply_to(
            message,
            "Добро пожаловать в погодный бот!\n\n"
            "Доступные команды:\n"
            "/weather или /today - текущая погода\n"
            "/forecast - прогноз на 3 дня\n"
            "/tomorrow - прогноз на завтра\n"
            "/refresh - обновить данные (сброс кеша)\n"
            "/help - справка",
            parse_mode="Markdown"
        )
    
    WeatherHandlers(bot, weather_service)
    
    logger.info(f"Бот запущен. Город: {config.CITY_NAME}")
    print(f"Бот запущен! Город: {config.CITY_NAME}")
    print("Доступные команды: /weather, /forecast, /tomorrow, /refresh")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()