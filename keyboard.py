from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
def get_keyboard(id):
    send_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Відправити ще",callback_data=F'send_to:{id}')]]
        )
    return send_keyboard

def get_keyboard_reply(id):
    send_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Відповісти",callback_data=F'reply_to:{id}')]]
        )
    return send_keyboard

def keyboard_share(id):
    url = f"https://t.me/share/url?url=➥https://t.me/Anonymous_ukraine_bot?start={id}"
    send_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Поділитись",url=url)]])
    return send_keyboard