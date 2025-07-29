import asyncio
import os
from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart,Command,CommandObject
from aiogram.fsm.state import StatesGroup,State
from aiogram.exceptions import TelegramAPIError
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from app.keyboard.keyboard import *
from app.config.config import BOT_USERNAME

from hashids import Hashids

main_router = Router()
class StateMessage(StatesGroup):
    message = State()

@main_router.message(CommandStart(deep_link=True))
async def start_ref(message:Message, cipher:Hashids,command:CommandObject,state:FSMContext):
    await state.set_state(StateMessage.message)
    await state.update_data(target_id=command.args)
    msg = """
Ви можете <b>анонімно</b> надіслати власнику цього посилання будь-що:
💬 текстове повідомлення, 📷 фото, 🎥 відео або 📎 файл.

Жодних імен, жодних акаунтів — ваша особа залишиться<b> повністю конфіденційною</b> 🔒
Сміливо діліться думками, враженнями чи просто передайте щось важливе 💭"""
    await message.reply(msg,parse_mode='html')
@main_router.message(StateMessage.message)
async def input_message(message:Message, cipher:Hashids,state:FSMContext):
    await state.update_data(message=message.text)
    await send_message(message=message,state=state,cipher=cipher)

async def send_message(message:Message, cipher:Hashids,state:FSMContext):
    data = await state.get_data()
    
    try:
        await state.clear()
        try:
            target_id = cipher.decode(data['target_id'])[0]
        except:
            await message.reply(
"""😬 Невалідне посилання!\nТакого користувача не існує!\nПереконайтесь що рефералка правильно надрукована
Якщо ви <b>впевнені</b> що посилання справне повідомте адміністратора!""",parse_mode="HTML")
            return
        keyboard = get_keyboard_reply(cipher.encode(message.from_user.id))
        caption_media = """
<b>📷️Отримано медіа!</b>\n
Для відповіді натисни на кнопку⤵"""
        match message.content_type:
            case ContentType.PHOTO:
                file_id = message.photo[-1].file_id
                await message.bot.send_photo(chat_id=target_id, photo=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.VIDEO:
                file_id = message.video.file_id
                await message.bot.send_video(chat_id=target_id, video=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.DOCUMENT:
                file_id = message.document.file_id
                await message.bot.send_document(chat_id=target_id, document=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.AUDIO:
                file_id = message.audio.file_id
                await message.bot.send_audio(chat_id=target_id, audio=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.ANIMATION:
                file_id = message.animation.file_id
                await message.bot.send_animation(chat_id=target_id, animation=file_id, caption=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.VOICE:
                file_id = message.voice.file_id
                await message.bot.send_voice(chat_id=target_id, voice=file_id, reply_markup=keyboard)
                await message.bot.send_message(chat_id=target_id, text=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.VIDEO_NOTE:
                file_id = message.video_note.file_id
                await message.bot.send_video_note(chat_id=target_id, video_note=file_id, reply_markup=keyboard)
                await message.bot.send_message(chat_id=target_id, text=caption_media, reply_markup=keyboard,parse_mode='html')
            case ContentType.STICKER:
                file_id = message.sticker.file_id
                await message.bot.send_sticker(chat_id=target_id, sticker=file_id, reply_markup=keyboard)
                await message.bot.send_message(chat_id=target_id, text=caption_media,parse_mode='html',reply_markup=keyboard)
            case ContentType.TEXT:
                caption_text = f'''<b>💬Отримано повідомлення!</b>\n{message.text}\n\n \nДля відповіді натисни на кнопку⤵'''
                await message.bot.send_message(chat_id=target_id, text=caption_text, reply_markup=keyboard,parse_mode='html')
            case _:
                await message.reply("🫨Невідомий тип даних")
                return
    except TelegramAPIError as e:
        await message.reply(f"😟Користувач не має відкритого чата з ботом...\nДеталі:{e}")
        return
    except Exception as e:
        
        await message.reply(f"😟Виникла помилка...\nДеталі:{e}")
        return
    await message.reply(
'<b>📦Повідомлення відправлено</b>,\nочікуйте відповідь',reply_markup=get_keyboard(data["target_id"]),parse_mode='HTML'
)    
@main_router.callback_query(F.data.startswith('send'))
async def callback_send(callback:CallbackQuery,state:FSMContext):
    _, type,target_id = callback.data.split(":")
    if type == "more":
        msg = "Надішліть повідомлення:"
    else:
        msg = "Відповідь"
    await state.set_state(StateMessage.message)
    await state.update_data(target_id=target_id)
    await callback.message.reply(msg)
    await callback.answer()
@main_router.message(Command(commands=['ref','start']))
async def ref(message:Message, cipher:Hashids):
    ref = cipher.encode(message.from_user.id)
    msg = f"""
Отримали своє <b>анонімне</b> посилання 🔗 — вставте його в профіль соцмереж, сторіз або біо.
Так друзі, підписники або навіть випадкові люди можуть анонімно надсилати повідомлення, фото, відео чи файли 🎥📸💬.

Це простий спосіб отримувати <b>чесний фідбек</b> і цікаві історії без розкриття особистих даних 🕵️‍♂️✨.
Діліться посиланням, будьте відкритими — і спостерігайте за сюрпризами, які приносить <b>анонімність! 🎉</b>\n
https://t.me/{BOT_USERNAME}?start={ref} - Поширюй цей <b>секретний код</b> і дивись, як відкривається новий рівень спілкування! 🚀
"""
    share_url = f"https://t.me/share/url?url=➥https://t.me/{BOT_USERNAME}?start={ref}"
    await message.reply(msg,reply_markup=keyboard_share(ref,share_url),parse_mode='html')