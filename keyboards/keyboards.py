from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from datetime import datetime, timedelta


def create_week_keyboard(start_date: datetime) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    days_buttons = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        button_text = day.strftime('%a %d')
        days_buttons.append(KeyboardButton(button_text))
    keyboard.row(*days_buttons)
    keyboard.row(
        KeyboardButton('⬅️ Предыдущая неделя'),
        KeyboardButton('Следующая неделя ➡️')
    )
    return keyboard


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
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday())  # Получить понедельник текущей недели
Week_kb = create_week_keyboard(start_of_week)
