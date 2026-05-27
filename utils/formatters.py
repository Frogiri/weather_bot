from models.weather import WeatherData

class WeatherFormatter:
    """Форматирование сообщений о погоде"""
    
    @staticmethod
    def format_current_weather(data: WeatherData) -> str:
        """Форматирует текущую погоду"""
        current = data.current
        
        # Эмодзи погоды
        weather_emoji = {
            "clear": "☀️",
            "cloud": "☁️",
            "rain": "🌧",
            "snow": "❄️",
            "thunderstorm": "⚡️"
        }
        
        emoji = "🌡"
        desc_lower = current.description.lower()
        if "ясно" in desc_lower or "clear" in desc_lower:
            emoji = weather_emoji["clear"]
        elif "облачно" in desc_lower or "cloud" in desc_lower:
            emoji = weather_emoji["cloud"]
        elif "дождь" in desc_lower or "rain" in desc_lower:
            emoji = weather_emoji["rain"]
        elif "снег" in desc_lower or "snow" in desc_lower:
            emoji = weather_emoji["snow"]
        elif "гроза" in desc_lower or "thunderstorm" in desc_lower:
            emoji = weather_emoji["thunderstorm"]
        
        return (
            f"🏙 *{data.city}*, {data.country}\n"
            f"{emoji} *{current.temp_celsius}* (ощущается как {current.feels_like_celsius})\n"
            f"📝 {current.description.capitalize()}\n"
            f"💧 Влажность: {current.humidity}%\n"
            f"🌬 Ветер: {current.wind_speed:.1f} м/с\n"
            f"📊 Давление: {current.pressure} гПа\n"
            f"🕐 Обновлено: {current.timestamp.strftime('%H:%M')}"
        )
    
    @staticmethod
    def format_forecast(data: WeatherData, days: int = 3) -> str:
        """Форматирует прогноз на несколько дней"""
        if not data.forecast:
            return "Прогноз недоступен"
        
        result = f"*Прогноз погоды для {data.city} на {days} дня:*\n\n"
        
        for i, day in enumerate(data.forecast[:days]):
            if i == 0:
                day_name = "Сегодня"
            elif i == 1:
                day_name = "Завтра"
            else:
                day_name = day.date.strftime("%A")
            
            result += (
                f"*{day_name}* ({day.date.strftime('%d.%m')}):\n"
                f"🌡 {day.temp_range}\n"
                f"📝 {day.description.capitalize()}\n"
                f"💧 Влажность: {day.humidity}%\n"
                f"🌬 Ветер: {day.wind_speed:.1f} м/с\n\n"
            )
        
        return result