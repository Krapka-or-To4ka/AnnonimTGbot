import asyncio
import os
from aiogram import Bot,Dispatcher,Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart,StateFilter,Command,CommandObject
from aiogram.fsm.state import StatesGroup,State
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from keyboard import *

from dotenv import load_dotenv
from hashids import Hashids
load_dotenv("key.env")
clipher =Hashids(salt=os.getenv("KEY"),min_length=8)
bot  = Bot("7659680233:AAH284AveoDlOLQoVxerCXkqug5k6dKV2J0")
dp = Dispatcher()
class StateMessage(StatesGroup):
    msg = State()

@dp.message(CommandStart(deep_link=True))
async def start_ref(msg:Message,command:CommandObject,state:FSMContext):
    await state.set_state(StateMessage.msg)
    await state.update_data(target_id=command.args)
    print(command.args)
    message = """
Ви можете <b>анонімно</b> надіслати власнику цього посилання будь-що:
💬 текстове повідомлення, 📷 фото, 🎥 відео або 📎 файл.

Жодних імен, жодних акаунтів — ваша особа залишиться<b> повністю конфіденційною</b> 🔒
Сміливо діліться думками, враженнями чи просто передайте щось важливе 💭"""
    await msg.reply(message,parse_mode='html')
@dp.message(StateMessage.msg)
async def input_msg(msg:Message,state:FSMContext):
    await state.update_data(msg=msg.text)
    await send_msg(msg=msg,state=state)

async def send_msg(msg:Message,state:FSMContext):
    data = await state.get_data()
    print(data)
    print(clipher.decode(data['target_id']))
    
    try:
        await state.clear()
        
        target_id = clipher.decode(data['target_id'])[0]
        keyboard = get_keyboard_reply(data['target_id'])
        print(keyboard)
        print(target_id)
        caption_media = """
<b>📷️Отримано медіа!</b>\n
Для відповіді натисни на кнопку⤵"""
        match msg.content_type:
            case ContentType.PHOTO:
                file_id = msg.photo[-1].file_id
                await msg.bot.send_photo(chat_id=target_id, photo=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.VIDEO:
                file_id = msg.video.file_id
                await msg.bot.send_video(chat_id=target_id, video=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.DOCUMENT:
                file_id = msg.document.file_id
                await msg.bot.send_document(chat_id=target_id, document=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.AUDIO:
                file_id = msg.audio.file_id
                await msg.bot.send_audio(chat_id=target_id, audio=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.ANIMATION:
                file_id = msg.animation.file_id
                await msg.bot.send_animation(chat_id=target_id, animation=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.VOICE:
                file_id = msg.voice.file_id
                await msg.bot.send_voice(chat_id=target_id, voice=file_id, reply_markup=keyboard)
                await msg.bot.send_message(chat_id=target_id, text=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.VIDEO_NOTE:
                file_id = msg.video_note.file_id
                await msg.bot.send_video_note(chat_id=target_id, video_note=file_id, reply_markup=keyboard)
                await msg.bot.send_message(chat_id=target_id, text=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.STICKER:
                file_id = msg.sticker.file_id
                await msg.bot.send_sticker(chat_id=target_id, sticker=file_id, reply_markup=keyboard)
                await msg.bot.send_message(chat_id=target_id, text=caption_media,parse_mode='html',reply_markup=keyboard)
            case ContentType.TEXT:
                caption_text = f'''<b>💬Отримано повідомлення!</b>\n{msg.text}\n\n \nДля відповіді натисни на кнопку⤵'''
                await msg.bot.send_message(chat_id=target_id, text=caption_text, reply_markup=keyboard,parse_mode='html')
            case _:
                msg.reply("🫨Невідомий тип даних")
    except:
        msg.reply("😟Виникла невідома помилка...")
    await msg.reply(
'<b>📦Повідомлення відправлено</b>,\nочікуйте відповідь',reply_markup=get_keyboard(data["target_id"]),parse_mode='HTML'
)    
@dp.callback_query(F.data.startswith('send_to:'))
async def callback_send(callback:CallbackQuery,state:FSMContext):
    target_id = callback.data.split(":")[1]
    await state.set_state(StateMessage.msg)
    await state.update_data(target_id=target_id)
    await callback.message.reply("Надішліть повідомлення:")
    await callback.answer()
@dp.callback_query(F.data.startswith('reply_to:'))
async def callback_send(callback:CallbackQuery,state:FSMContext):
    target_id = callback.data.split(":")[1]
    await state.set_state(StateMessage.msg)
    await state.update_data(target_id=target_id)
    await callback.message.reply("Ваша відповідь:")
    await callback.answer()

'''
@dp.message(CommandStart())
async def start(msg:Message):
    ref = clipher.encode(msg.from_user.id)
    message = f"""
Отримали своє <b>анонімне</b> посилання 🔗 — вставте його в профіль соцмереж, сторіз або біо.
Так друзі, підписники або навіть випадкові люди можуть анонімно надсилати повідомлення, фото, відео чи файли 🎥📸💬.

Це простий спосіб отримувати <b>чесний фідбек</b> і цікаві історії без розкриття особистих даних 🕵️‍♂️✨.
Діліться посиланням, будьте відкритими — і спостерігайте за сюрпризами, які приносить <b>анонімність! 🎉</b>\n
https://t.me/Anonymous_ukraine_bot?start={ref} - Поширюй цей <b>секретний код</b> і дивись, як відкривається новий рівень спілкування! 🚀
"""
    await msg.reply(message,reply_markup=keyboard_share(ref),parse_mode='html')'''
@dp.message(Command(commands=['ref','start']))
async def ref(msg:Message):
    ref = clipher.encode(msg.from_user.id)
    message = f"""
Отримали своє <b>анонімне</b> посилання 🔗 — вставте його в профіль соцмереж, сторіз або біо.
Так друзі, підписники або навіть випадкові люди можуть анонімно надсилати повідомлення, фото, відео чи файли 🎥📸💬.

Це простий спосіб отримувати <b>чесний фідбек</b> і цікаві історії без розкриття особистих даних 🕵️‍♂️✨.
Діліться посиланням, будьте відкритими — і спостерігайте за сюрпризами, які приносить <b>анонімність! 🎉</b>\n
https://t.me/Anonymous_ukraine_bot?start={ref} - Поширюй цей <b>секретний код</b> і дивись, як відкривається новий рівень спілкування! 🚀
"""
    await msg.reply(message,reply_markup=keyboard_share(ref),parse_mode='html')
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())