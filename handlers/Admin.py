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
    user_id = State()
    service = State()
    price = State()
    date_app = State()
    time_app = State()


async def start(message: types.Message):
    if message.from_user.id in config.admins:
        await message.answer('Вы открыли панель администратора', parse_mode="HTML", reply_markup=AdminPanel)


async def add_user(message: types.Message):
    await message.answer('Введите имя клиента')
    await Users.user.set()


async def add_user_phone(message: types.Message, state):
    if _data_.check_name(message.text)["success"]:
        await state.update_data(name=message.text)
        await message.answer(text='Введите номер телефона клиента')
        await Users.phone.set()
    else:
        await message.answer(text='Клиент с таким именем уже существует , введите другое имя')
        await Users.user.set()


async def send_user(message: types.Message, state):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    username, user_phone = data['name'], int(data['phone'])
    if _data_.add_client(username, user_phone)["success"]:
        await message.answer(
            text=f'Клиент {username} с номером телефона {user_phone} добавлен!', parse_mode='HTML'
        )
        await state.finish()
    else:
        await message.answer(
            text=f'Клиент с номером телефона <b>{user_phone}</b> уже существует в базе!', parse_mode='HTML'
        )
        await state.finish()


async def add_service(message: types.Message):
    await message.answer('Введите название услуги')
    await Users.service.set()


async def add_service_price(message: types.Message, state):
    if _data_.check_service(message.text)["success"]:
        await state.update_data(service=message.text)
        await message.answer(text='Введите цену услуги')
        await Users.price.set()
    else:
        await message.answer(
            text='Услуга с таким названием существует в базе, хотите изменить её цену ?', reply_markup=Choice
        )


async def send_service(message: types.Message, state):
    await state.update_data(price=message.text)
    data = await state.get_data()
    service_name, price = data['service'], int(data['price'])
    if _data_.check_service(service_name)["success"]:
        _data_.add_service(service_name, price)
        print(_data_.add_service(service_name, price)["message"])
        await message.answer('Услуга добавлена')
        await state.finish()
    else:
        _data_.update_service(service_name, price)
        await message.answer('Цена изменена')
        await state.finish()


async def get_ID_step_1(message: types.Message):
    await message.answer('Введите имя или номер телефона клиента')
    await Users.user_id.set()


async def get_ID_step_2(message: types.Message, state):
    if str(message.text).isdigit():
        client_id = _data_.get_id(int(message.text))
    else:
        client_id = _data_.get_id(message.text)
    if client_id and 'values' in client_id:
        await message.answer(f"ID клиента : {client_id['values']}")
        await state.finish()
    else:
        await message.answer("Клиент не найден или ошибка при получении данных")
        await state.finish()
