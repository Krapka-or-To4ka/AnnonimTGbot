from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart,StateFilter,Command
from hashids import Hashids
from app.database.manager_user import Manager
import asyncio
import logging
from app.logging.loggin_init import setup_logger
logger = logging.getLogger(__name__)
setup_logger(logger)
admin_router = Router()

@admin_router.message(Command('decode'))
async def decode(message:Message,cipher:Hashids):
    args = message.text.split()

    if len(args) == 2:
        id = cipher.decode(args[1])[0]
        url = f"tg://user?id={id}"
        await message.reply(f"{url}\nid:{id}")

    else:
        await message.reply("Повинно бути два аргументи")

@admin_router.message(Command('info'))
async def info(message:Message,user_manager:Manager):

    msg = f'''
id:{message.bot.id}
Всього користувачів:{await user_manager.count_user()}
'''
    await message.reply(msg)

@admin_router.message(Command("send"))
async def send(message:Message,user_manager:Manager):
    if len(message.text.split()) != 3 and message.reply_to_message is None:
        await message.reply("Не вірний формат\n Формат: \\send (to(id or 'all')) (time_delay(second))")
        return
    _, to,time = message.text.split()
    if to == 'all':
        ids = await user_manager.all_user()
    else:
        ids = [to]
    logger.debug(f"ВСІ АЙДІ:{ids}")
    bad_account = 0
    god_account = 0 
    for i in ids:
        try:
            await message.bot.copy_message(
    chat_id=i,from_chat_id=message.from_user.id,message_id=message.reply_to_message.message_id)
            god_account += 1
        except:
            bad_account += 1
        asyncio.sleep(time)
    await message.reply(f"Успішно переслано!\nУспішно:{god_account}\nНеуспішно{bad_account}")

