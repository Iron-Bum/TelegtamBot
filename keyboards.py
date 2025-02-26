from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

AdminPanel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запись', callback_data='booking'),
            KeyboardButton(text='Добавить клиента')
        ],
        [
            KeyboardButton(text='Добавить (редактировать) услугу'),
            KeyboardButton(text='Статистика', callback_data='statistic'),
            KeyboardButton(text='Получить ID', callback_data='get_ID')
        ],
    ], resize_keyboard=True
)