from telebot import TeleBot
from telebot.types import Message
from core.weather_service import WeatherService
from utils.formatters import WeatherFormatter
from loguru import logger

class WeatherHandlers:
    """Обработчики команд погоды"""
    
    def __init__(self, bot: TeleBot, weather_service: WeatherService):
        self.bot = bot
        self.weather_service = weather_service
        self._register_handlers()
    
    def _register_handlers(self):
        """Регистрирует команды"""
        @self.bot.message_handler(commands=["weather", "today"])
        def today_command(message: Message):
            self.send_current_weather(message)
        
        @self.bot.message_handler(commands=["forecast"])
        def forecast_command(message: Message):
            self.send_forecast(message)
        
        @self.bot.message_handler(commands=["tomorrow"])
        def tomorrow_command(message: Message):
            self.send_tomorrow(message)
        
        @self.bot.message_handler(commands=["refresh"])
        def refresh_command(message: Message):
            self.refresh_weather(message)
    
    def send_current_weather(self, message: Message):
        """Отправляет текущую погоду"""
        chat_id = message.chat.id
        
        with self.bot.send_chat_action(chat_id, 'typing'):
            weather_data = self.weather_service.get_weather()
            
            if not weather_data:
                self.bot.reply_to(message, "Не удалось получить данные о погоде. Попробуйте позже...")
                return
            
            text = WeatherFormatter.format_current_weather(weather_data)
            self.bot.send_message(chat_id, text, parse_mode="Markdown")
    
    def send_forecast(self, message: Message):
        """Отправляет прогноз на 3 дня"""
        chat_id = message.chat.id
        
        with self.bot.send_chat_action(chat_id, 'typing'):
            weather_data = self.weather_service.get_weather()
            
            if not weather_data:
                self.bot.reply_to(message, "Не удалось получить прогноз.")
                return
            
            text = WeatherFormatter.format_forecast(weather_data, days=3)
            self.bot.send_message(chat_id, text, parse_mode="Markdown")
    
    def send_tomorrow(self, message: Message):
        """Отправляет прогноз на завтра"""
        chat_id = message.chat.id
        
        with self.bot.send_chat_action(chat_id, 'typing'):
            weather_data = self.weather_service.get_weather()
            
            if not weather_data or len(weather_data.forecast) < 2:
                self.bot.reply_to(message, "Нет данных на завтра.")
                return
            
            tomorrow = weather_data.forecast[1]
            text = (
                f"📅 *Завтра в {weather_data.city}:*\n"
                f"🌡 {tomorrow.temp_range}\n"
                f"📝 {tomorrow.description.capitalize()}\n"
                f"💧 Влажность: {tomorrow.humidity}%\n"
                f"🌬 Ветер: {tomorrow.wind_speed:.1f} м/с"
            )
            self.bot.send_message(chat_id, text, parse_mode="Markdown")
    
    def refresh_weather(self, message: Message):
        """Принудительное обновление кеша"""
        chat_id = message.chat.id
        
        with self.bot.send_chat_action(chat_id, 'typing'):
            self.weather_service.clear_cache()
            weather_data = self.weather_service.get_weather(force_refresh=True)
            
            if weather_data:
                self.bot.reply_to(message, "Данные о погоде обновлены!")
            else:
                self.bot.reply_to(message, "Не удалось обновить данные.")