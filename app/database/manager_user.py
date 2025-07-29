import logging
from aiogram.types import Message
import asyncpg
from hashids import Hashids
from app.database.database_init import DataBase
from typing import Optional
from app.logging.loggin_init import setup_logger
logger = logging.getLogger(__name__)
setup_logger(logger)
class Manager:
    def __init__(self,db:DataBase):
        self.db:DataBase|None = db
        if self.db is None:
            logger.debug("Database не підключена")
            self.disabled = True
        else:
            self.pool = self.db.get_pool()
            self.disabled = False

    async def create_table(self):
        if self.disabled: return
        logger.debug("Зроблена таблиця")
        async with self.pool.acquire() as conn:
            await conn.execute("""
CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY,
                            username TEXT,
                            first_name TEXT,
                            last_name TEXT,
                            language_gui TEXT,
                            is_premium BOOL,
                            encode_id TEXT)""")

    async def create_user(self,message:Message,cipher:Hashids):
        if self.disabled: return
        async with self.pool.acquire() as conn:
            user = message.from_user
            await conn.fetchval(
"""
INSERT INTO users(id,username,first_name,last_name,language_gui,is_premium,encode_id) VALUES (
$1,$2,$3,$4,$5,$6,$7)
ON CONFLICT(id) DO UPDATE SET
    username = EXCLUDED.username,
    first_name= EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    language_gui = EXCLUDED.language_gui,
    is_premium = EXCLUDED.is_premium,
    encode_id = EXCLUDED.encode_id""",
user.id,user.username,user.first_name,user.last_name,user.language_code,user.is_premium,cipher.encode(user.id))
            logger.debug(f"Користувач {user.id} зареєстрований у бд ")
    async def count_user(self):
        if self.disabled: return
        async with self.pool.acquire() as conn:
            logger.debug("Порахував кількість користувачів")
            result = await conn.fetchval("SELECT COUNT(id)FROM users ")
            return result
    async def all_user(self):
        if self.disabled: return
        async with self.pool.acquire() as conn:
            result = await conn.fetch("SELECT id FROM users")
            logger.debug("Айді всіх в бд Зібрані та передані")
            ids = [account['id'] for account in result ]
            return ids