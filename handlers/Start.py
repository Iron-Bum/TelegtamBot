import sys
import os
from aiogram import types
from keyboards.StartKeyboard import *
from keyboards.ClientKeyboard import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from DataBaseManager import DataBase
from aiogram.dispatcher import FSMContext
sys.path.append(os.path.join(os.getcwd(), '..'))


db = DataBase('database/tables.db')
db.connect()


class Registration(StatesGroup):
    name = State()
    phone = State()


async def hi(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Добро пожаловать', reply_markup=StartPanel)


async def registration_step1(message: types.Message):
    telegram_id = message.from_user.id
    if db.clients.check_telegram_id(telegram_id)['success']:
        await message.answer('Напишите ваше имя')
        await Registration.name.set()
    else:
        await message.answer(f'Здравствуй {message.from_user.username}', reply_markup=ClientPanel)


async def registration_step2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        f'<em>Вы указали имя:</em> <b>{message.text}</b>\n<b>Поделитесь своим номером телефона </b>',
        parse_mode='HTML',
        reply_markup=ShareANumberPanel
    )
    await Registration.phone.set()


async def registration_step3(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    name = data['name']
    db.clients.add_client(name, phone_number, message.from_user.id)
    await message.answer('Вы зарегестрированы!', reply_markup=ClientPanel)
    await state.finish()
