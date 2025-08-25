from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Optional
from datetime import datetime, timedelta
from Database_T_Bot import Database


class WeekKeyboardManager:
    def __init__(self, start_date: datetime = None):
        if start_date is None:
            today = datetime.now()
            self.start_date = today - timedelta(days=today.weekday())  # понедельник текущей недели
        else:
            self.start_date = start_date

    def create_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        days_buttons = []
        for i in range(7):
            day = self.start_date + timedelta(days=i)
            button_text = day.strftime('%d.%m')
            days_buttons.append(KeyboardButton(button_text))
        keyboard.row(*days_buttons)
        keyboard.row(
            KeyboardButton('⬅️ Предыдущая неделя'),
            KeyboardButton('Следующая неделя ➡️')
        )
        return keyboard

    def go_next_week(self):
        self.start_date += timedelta(days=7)

    def go_prev_week(self):
        self.start_date -= timedelta(days=7)


class DayKeyboardManager:
    def __init__(self, db: Database):
        self.db = db  # экземпляр вашего класса Database

    def create_time_keyboard(self, date: datetime) -> Optional[ReplyKeyboardMarkup]:
        free_times = self.db.get_list_free_time(date)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [KeyboardButton(time.strftime('%H:%M')) for time in free_times]
        # Добавляем кнопки по 4 в строку
        if buttons:
            row = []
            for i, button in enumerate(buttons, start=1):
                row.append(button)
                if i % 4 == 0:
                    keyboard.row(*row)
                    row = []
            # Добавляем оставшиеся кнопки, если они есть
            if row:
                keyboard.row(*row)
            return keyboard
        return None
