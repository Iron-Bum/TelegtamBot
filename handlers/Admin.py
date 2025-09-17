from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
import config
from keyboards.AdminKeyboard import *
import sys
import os
import Database_T_Bot
from appointment.appointment import Master, Client, Service, Appointment

sys.path.append(os.path.join(os.getcwd(), '..'))

db = Database_T_Bot.Database('tables.db')
db.connect()
db.create_tables()
db.create_schedule('Ин')
db.del_old_free_time()


class UserState(StatesGroup):
    name = State()
    phone = State()
    user_id = State()


class ServiceState(StatesGroup):
    name = State()
    cost = State()


class MasterState(StatesGroup):
    name = State()


class BookingState(StatesGroup):
    choosing_date = State()
    choosing_time = State()


async def start(message: types.Message):
    if message.from_user.id in config.admins:
        await message.answer('Вы открыли панель администратора', parse_mode="HTML", reply_markup=AdminPanel)


async def add_master(message: types.Message):
    await message.answer('Введите имя мастера')
    await MasterState.name.set()


async def send_master(message: types.Message, state: FSMContext):
    db.add_master(Master(message.text))
    await message.answer(f'{message.text} добавлен!')
    await state.finish()


async def add_user(message: types.Message):
    await message.answer('Введите имя клиента')
    await UserState.name.set()


async def add_user_phone(message: types.Message, state: FSMContext):
    if db.check_name(message.text)["success"]:
        await state.update_data(name=message.text)
        await message.answer(text='Введите номер телефона клиента')
        await UserState.phone.set()
    else:
        await message.answer(text='Клиент с таким именем уже существует , введите другое имя')
        await UserState.name.set()


async def send_user(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    username, user_phone = data['name'], data['phone']
    if db.add_client(username, user_phone, message.from_user.id)["success"]:
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
    await ServiceState.name.set()


async def add_service_price(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    if db.check_service(message.text)["success"]:
        await message.answer(text='Введите цену услуги')
        await ServiceState.cost.set()
    else:
        await message.answer(
            text='Услуга с таким названием существует в базе, хотите изменить её цену ?', reply_markup=Choice
        )


async def hendl_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'choice_yes':
        await call.message.answer('Введите новую цену услуги')
        await ServiceState.cost.set()
    elif call.data == 'choice_nou':
        await call.message.answer('Операция отменена.')
        await state.finish()
    await call.answer()


async def send_service(message: types.Message, state: FSMContext):
    try:
        await state.update_data(price=message.text)
        data = await state.get_data()
        service_name, price = data['service'], int(data['price'])
        if db.check_service(service_name)["success"]:
            service = Service(service_name, price)
            db.add_service(service)
            await message.answer('Услуга добавлена')
        else:
            db.upd_price(service_name, price)
            await message.answer('Цена изменена')
        await state.finish()
    except ValueError:
        await state.finish()
        await message.answer(text=f'Ошибка, попробуйте заново', reply_markup=AdminPanel)


async def get_client_id_step_1(message: types.Message):
    await message.answer('Введите имя или номер телефона клиента')
    await UserState.user_id.set()


async def get_client_id_step_2(message: types.Message, state: FSMContext):
    client_id = db.get_client_id(message.text)
    if 'values' in client_id:
        await message.answer(f"ID клиента : {client_id['values']}")
        await state.finish()
    else:
        await message.answer(f"{client_id['message']}")
        await state.finish()
