from telebot import TeleBot
from telebot.types import Message

class MessageHandlers:
    """Обработчики обычных сообщений (не команд)"""
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self._register_handlers()
    def _register_handlers(self):
        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message: Message):
            self.bot.reply_to(
                message, 
                "Неизвестная команда. Напиши /help для списка команд."
            )