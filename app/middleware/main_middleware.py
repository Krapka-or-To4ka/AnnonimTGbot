from aiogram import BaseMiddleware
from aiogram.types import Message,CallbackQuery
from cachetools import TTLCache
from app.database.manager_user import Manager
import logging
from app.logging.loggin_init import setup_logger
logger = logging.getLogger(__name__)
setup_logger(logger)
#ставе ліміт та передає залежності
class MainMiddleware(BaseMiddleware):

    def __init__(self,limit,cipher,db,manager:Manager):
        logger.debug(F"ІНІЦІАЛІЗІЦІЯ{self.__class__.__name__}")
        self.limit = limit
        self.__users_using = TTLCache(maxsize=20_000,ttl=60)
        self.cipher = cipher
        self.db = db
        self.manager = manager
    async def __call__(self, handler, event, data):
        logger.debug(f"{self.__class__.__name__} Отримано запит")
        msg = 'Ви перевисили кількість запитів на хвилину'
        command_notify = event.reply if isinstance(event, Message) else event.message.reply
        user_id = event.from_user.id
        count = self.__users_using.get(user_id,0)
        if count ==  self.limit:
            logger.debug("СПОВІЩЕННЯ ПРО ЛІМІТ")
            await command_notify(msg)
            logger.debug(f"ЗАРАХОВАНИЙ ЗАПИТ {self.__class__.__name__}")
            self.__users_using[user_id] = count+1
        elif count < self.limit:
            self.__users_using[user_id] = count+1
            data['cipher'] = self.cipher
            data['user_manager'] = self.manager
            logger.debug(f"ЗАПИТ ОДОБРЕН{self.__class__.__name__}")
            await handler(event, data)
            logger.debug("ХЕНДЛЕР ЗАКІНЧИВ РОБОТУ")
            await self.manager.create_user(message=event,cipher=self.cipher)    
        else:
            logger.debug(f"{event.from_user.id} ЗАПИТ Пропускаємо")
        return
        