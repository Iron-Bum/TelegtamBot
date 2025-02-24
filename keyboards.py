from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

AdminPanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Запись', callback_data='booking'),
            InlineKeyboardButton(text='Добавить клиента', callback_data='add_user')
        ],
        [
            InlineKeyboardButton(text='Добавить (редактировать) услугу', callback_data='add_service'),
            InlineKeyboardButton(text='Статистика', callback_data='statistic')
        ],
    ]
)