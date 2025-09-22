import sys
import os
from aiogram import types
from keyboards.ClientKeyboard import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.KeyboardManager import *
from handlers.Start import db
sys.path.append(os.path.join(os.getcwd(), '..'))

manager_dey = DayKeyboardManager(db)


class BookingState(StatesGroup):
    choosing_date = State()
    choosing_time = State()


async def menu(message: types.Message):
    await message.answer(text='Меню', reply_markup=ClientPanel)


async def start_choice_date(message: types.Message, state: FSMContext):
    manager_week = WeekKeyboardManager()
    await state.update_data(start_date=manager_week.start_date.isoformat())
    keyboard = manager_week.create_keyboard()
    await message.answer("Выберите дату недели:", reply_markup=keyboard)
    await BookingState.choosing_date.set()


async def week_navigation_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    start_date_str = user_data.get('start_date')
    start_date = datetime.fromisoformat(start_date_str)
    manager_week = WeekKeyboardManager(start_date)
    text = 'Выберите дату недели: '
    # Обработка кнопок навигации
    if message.text == 'Следующая неделя ➡️':
        manager_week.go_next_week()
    elif message.text == '⬅️ Предыдущая неделя':
        manager_week.go_prev_week()
    elif message.text == 'Отмена 🚫':
        await state.finish()
        await message.answer('Меню', reply_markup=ClientPanel)
        return
    else:
        try:
            # Обработка выбора конкретной даты
            chosen_date_str = f"{message.text}.{datetime.now().year}"
            chosen_date = datetime.strptime(chosen_date_str, "%d.%m.%Y")
            await state.update_data(chosen_date=chosen_date)
            time_kb = manager_dey.create_time_keyboard(chosen_date)
            if time_kb:
                await message.answer('Выберите свободное время:', reply_markup=time_kb)
                await BookingState.choosing_time.set()
                return
            else:
                text = 'На выбранную дату нет свободного времени, выберите другой день.'
        except Exception as e:
            text = f'Ошибка {e}, повторите попытку'

    # Обновляем состояние и клавиатуру
    await state.update_data(start_date=manager_week.start_date.isoformat())
    keyboard = manager_week.create_keyboard()
    await message.answer(text, reply_markup=keyboard)


async def day_navigation_handler(message: types.Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        day = user_data.get('chosen_date')
        # Обработка выбора времени в формат datatime
        chosen_datatime_str = f"{day.strftime('%Y-%m-%d')} {message.text}"
        chosen_datatime = datetime.strptime(chosen_datatime_str, "%Y-%m-%d %H:%M")
        await message.answer(f'Запись на {chosen_datatime} зарезервирована', reply_markup=ClientPanel)
        db.bookings.add_booking(1, 2, chosen_datatime_str)
        await state.finish()
    except ValueError:
        await state.finish()
        await message.answer(text=f'Ошибка, попробуйте заново', reply_markup=ClientPanel)
