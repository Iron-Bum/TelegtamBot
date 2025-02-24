from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import config
from keyboards import *
import sys
import os
from Database_T_Bot import _data_
sys.path.append(os.path.join(os.getcwd(), '..'))


class Users(StatesGroup):
    user = State()
    phone = State()
    service = State()
    date_app = State()
    time_app = State()


async def start(message):
    if message.from_user.id in config.admins:
        await message.answer('Вы открыли панель администратора', parse_mode="HTML", reply_markup=AdminPanel)


async def add_user(call):
    await call.message.answer('Введите имя клиента')
    await Users.user.set()
    await call.answer()


async def add_user_phone(message, state):
    if _data_.check_name(message.text)["success"]:
        await state.update_data(name=message.text)
        await message.answer(text='Введите номер телефона клиента')
        await Users.phone.set()
    else:
        await message.answer(text='Клиент с таким именем уже существует , введите другое имя')
        await Users.user.set()

async def send_user(message, state):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    username, user_phone = data['name'], int(data['phone'])
    if _data_.add_client(username, user_phone)["success"]:
        await message.answer(f'Клиент {username} с номером телефона {user_phone} добавлен!', parse_mode='HTML')
        await state.finish()
    else:
        await message.answer(f'Клиент с номером телефона <b>{user_phone}</b> уже существует в базе!', parse_mode='HTML')
        await state.finish()

