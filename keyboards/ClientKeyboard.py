from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ClientPanel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запись ✍🏻📅'),
            KeyboardButton(text='Отменить запись 🙅')
        ]
    ]
)