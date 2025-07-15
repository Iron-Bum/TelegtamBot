from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
import config
from keyboards import *
import sys
import os
import Database_T_Bot

sys.path.append(os.path.join(os.getcwd(), '..'))

db = Database_T_Bot.Database('tables.db')
db.connect()
db.create_tables()
db.create_schedule('Ин')


class User(StatesGroup):
    name = State()
    phone = State()
    user_id = State()


class Service(StatesGroup):
    name = State()
    cost = State()


class Master(StatesGroup):
    name = State()


async def start(message: types.Message):
    if message.from_user.id in config.admins:
        await message.answer('Вы открыли панель администратора', parse_mode="HTML", reply_markup=AdminPanel)


async def add_master(message: types.Message):
    await message.answer('Введите имя мастера')
    await Master.name.set()


async def send_master(message: types.Message, state: FSMContext):
    db.add_master(message.text)
    await message.answer(f'{message.text} добавлен!')
    await state.finish()


async def add_user(message: types.Message):
    await message.answer('Введите имя клиента')
    await User.name.set()


async def add_user_phone(message: types.Message, state):
    if db.check_name(message.text)["success"]:
        await state.update_data(name=message.text)
        await message.answer(text='Введите номер телефона клиента')
        await User.phone.set()
    else:
        await message.answer(text='Клиент с таким именем уже существует , введите другое имя')
        await User.name.set()


async def send_user(message: types.Message, state):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    username, user_phone = data['name'], int(data['phone'])
    if db.add_client(username, user_phone)["success"]:
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
    await Service.name.set()


async def add_service_price(message: types.Message, state):
    await state.update_data(service=message.text)
    if db.check_service(message.text)["success"]:
        await message.answer(text='Введите цену услуги')
        await Service.cost.set()
    else:
        await message.answer(
            text='Услуга с таким названием существует в базе, хотите изменить её цену ?', reply_markup=Choice
        )


async def hendl_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'choice_yes':
        await call.message.answer('Введите новую цену услуги')
        await Service.cost.set()
    elif call.data == 'choice_nou':
        await call.message.answer('Операция отменена.')
        await state.finish()
    await call.answer()


async def send_service(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    service_name, price = data['service'], int(data['price'])
    print(service_name, price)
    if db.check_service(service_name)["success"]:
        db.add_service(service_name, price)
        await message.answer('Услуга добавлена')
    else:
        db.upd_price(service_name, price)
        await message.answer('Цена изменена')
    await state.finish()


async def get_client_id_step_1(message: types.Message):
    await message.answer('Введите имя или номер телефона клиента')
    await User.user_id.set()


async def get_client_id_step_2(message: types.Message, state: FSMContext):
    if str(message.text).isdigit():
        client_id = db.get_client_id(int(message.text))
    else:
        client_id = db.get_client_id(message.text)
    if 'values' in client_id:
        await message.answer(f"ID клиента : {client_id['values']}")
        await state.finish()
    else:
        await message.answer(f"{client_id['message']}")
        await state.finish()
