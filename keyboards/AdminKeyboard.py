from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

AdminPanel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить клиента'),
            KeyboardButton(text='Добавить мастера')
        ],
        [
            KeyboardButton(text='Добавить (редактировать) услугу'),
            KeyboardButton(text='Статистика'),
            KeyboardButton(text='Получить ID')
        ]], resize_keyboard=True
)
Choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Нет', callback_data='choice_nou'),
            InlineKeyboardButton(text='Да', callback_data='choice_yes')
        ]], resize_keyboard=True
)
