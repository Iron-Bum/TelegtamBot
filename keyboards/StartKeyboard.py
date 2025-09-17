from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

StartPanel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вход/Регистрация', callback_data='registration'),
            KeyboardButton(text='О нас', callback_data='about')
        ],
        [
            KeyboardButton(text='Цены', callback_data='price'),
            KeyboardButton(text='Админ')
        ]
    ], resize_keyboard=True
)
ShareANumberPanel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поделиться 📡📲', parse_mode='HTML', request_contact=True),
            KeyboardButton(text='Прервать регистрацию 🚫')

        ]
    ], resize_keyboard=True, one_time_keyboard=True
)