from aiogram import BaseMiddleware
from aiogram.types import Message,CallbackQuery
from cachetools import TTLCache
from os import getenv
from dotenv import load_dotenv
import logging
from app.logging.loggin_init import setup_logger
logger = logging.getLogger(__name__)
setup_logger(logger)


class AdminMiddleware(BaseMiddleware):
    def __init__(self,admins:list):
        logger.debug(f"ініціалізація:{self.__class__.__name__}")
        self.admins = list(map(int,admins))
        logger.debug(f"Адміни:{self.admins}")
    async def __call__(self, handler, event, data):
        logger.debug(f"Виклик {self.__class__.__name__}")
        user_id = event.from_user.id
        if user_id in self.admins:
            logger.debug(f"Користувач є адміном")
            return await handler(event,data)
        else:
            logger.debug("Користувач не є адміном")
            return