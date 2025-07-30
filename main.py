import asyncio
import os
from aiogram import Bot,Dispatcher,Router,F
from app.middleware.main_middleware import MainMiddleware
from app.middleware.admin_middleware import AdminMiddleware
from app.handlers.main_hand import main_router
from app.handlers.admin_hand import admin_router
from dotenv import load_dotenv
from hashids import Hashids
from app.database.database_init import DataBase
from app.database.manager_user import Manager
from app.config.config import IS_USING_DB,LIMIT_HANDLERS,LIMIT_CALLBACK
load_dotenv("key.env")
import logging
from app.logging.loggin_init import setup_logger
logger = logging.getLogger(__name__)
setup_logger(logger)

def get_info_bot():
    
    cipher =Hashids(salt=os.getenv("KEY"),min_length=8)
    bot  = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()
    admins = list(map(int,(os.getenv('Admins').split("."))))
    if IS_USING_DB:
        port = int(os.getenv("PORT"))
        host = os.getenv("HOST")
        user = os.getenv("USER")
        database = os.getenv("DATABASE")
        password = os.getenv("PASSWORD")
        if not all([host, user, database, password]):
            logger.debug("НЕВДАЛОСЯ ОТРИМАТИ ДАНІ ПРО БАЗУ ДАНИХ З ENV")
            logger.debug("Запускаємо без DataBase")
            db = None
        else:
            logger.debug("env успішно зчитан")
            db = DataBase(user=user,host=host,port=port,password=password,database=database)
    else:
        db = None
    return {"cipher":cipher,'bot':bot,"dp":dp,"admins":admins,'db':db}

async def get_manager(db:DataBase):
    if not (db is None):
        await db.connect() # вмикаємо бд та робимо пул
    manager_user = Manager(db)
    await manager_user.create_table()
    # замість _ буде інший менеджер поки як затичка 
    return (manager_user,'_')

async def main(cipher,bot,dp,admins,db:DataBase): 
    '_______РОБИМО МЕСЕНДЖЕРИ ДЛЯ УПРАВЛІНЯ БД______'
    manager_user,_ = await get_manager(db)
    dp.message.middleware(MainMiddleware(cipher=cipher,limit=LIMIT_HANDLERS,db=db,manager=manager_user))
    admin_router.message.middleware(AdminMiddleware(admins))
    dp.callback_query.middleware(MainMiddleware(cipher=cipher,limit=LIMIT_CALLBACK,db=db,manager=manager_user))


    
    dp.include_router(main_router)
    dp.include_router(admin_router)
    
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Закриваємо програму....")
        if not (db is None):
            await db.close()
            logger.info("БД ЗАКРИТА")

if __name__ == "__main__":
    try:
        asyncio.run(main(**get_info_bot()))
    except KeyboardInterrupt:
        logger.debug("---- Програма Завершена ----")