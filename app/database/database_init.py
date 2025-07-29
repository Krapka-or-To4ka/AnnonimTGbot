import logging
from aiogram.types import Message
import asyncpg
from hashids import Hashids
from app.logging.loggin_init import setup_logger
logger = logging.getLogger(__name__)
setup_logger(logger)
class DataBaseError(Exception):
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
class DataBase:
    def __init__(self,user,password,database,host,port=5432):
        self.dsn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.pool : asyncpg.Pool = None
    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(self.dsn,min_size=1,max_size=10)
            logger.debug(f"Підключення до {self.dsn} успішне")
        except:
            logger.debug(f'Не вдалося підключити {self.dsn}')
    def get_pool(self):
        if self.pool:
            return self.pool
        else:
            logging.critical("Пул не зроблен")
            raise DataBaseError(f"Пул не зроблен{self.__class__.__name__}")
    async def close(self):
        await self.pool.close()

