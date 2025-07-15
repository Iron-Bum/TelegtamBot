from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

AdminPanel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запись', callback_data='booking'),
            KeyboardButton(text='Добавить клиента'),
            KeyboardButton(text='Добавить мастера')
        ],
        [
            KeyboardButton(text='Добавить (редактировать) услугу'),
            KeyboardButton(text='Статистика', callback_data='statistic'),
            KeyboardButton(text='Получить ID', callback_data='get_ID')
        ]], resize_keyboard=True
)
Choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Нет', callback_data='choice_nou'),
            InlineKeyboardButton(text='Да', callback_data='choice_yes')
        ]], resize_keyboard=True
)