import aiogram
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputMediaPhoto
import config
from handlers import Admin, Start, Client
import database

api = config.API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.message_handler(Text(equals=['Админ']))(Admin.start)
dp.message_handler(Text(equals=['Вход/Регистрация']))(Start.registration_step1)
dp.callback_query_handler(text=['choice_yes', 'choice_nou'], state=Admin.ServiceState.name)(Admin.hendl_choice)
dp.message_handler(Text(equals=['Прервать регистрацию 🚫']), state=Start.Registration.phone)(Start.hi)
dp.message_handler(Text(equals=['Добавить клиента 👩🏻‍🦰']))(Admin.add_user)
dp.message_handler(Text(equals=['Добавить услугу 💰🫰🏻']))(Admin.add_service)
dp.message_handler(Text(equals=['Получить ID']))(Admin.get_client_id_step_1)
dp.message_handler(Text(equals=['Добавить мастера 💇🏻‍♀️']))(Admin.add_master)
dp.message_handler(Text(equals=['Запись']))(Client.start_choice_date)
dp.message_handler(Text(equals=['Отмена']))(Client.menu)
dp.message_handler(state=Start.Registration.name)(Start.registration_step2)
dp.message_handler(state=Start.Registration.phone, content_types=types.ContentType.CONTACT)(Start.registration_step3)
dp.message_handler(state=Admin.UserState.user_id)(Admin.get_client_id_step_2)
dp.message_handler(state=Admin.MasterState.name)(Admin.send_master)
dp.message_handler(state=Admin.UserState.name)(Admin.add_user_phone)
dp.message_handler(state=Admin.UserState.phone)(Admin.send_user)
dp.message_handler(state=Admin.ServiceState.name)(Admin.add_service_price)
dp.message_handler(state=Admin.ServiceState.cost)(Admin.send_service)
dp.message_handler(state=Admin.BookingState.choosing_date)(Client.week_navigation_handler)
dp.message_handler(state=Admin.BookingState.choosing_time)(Client.day_navigation_handler)
dp.message_handler()(Start.hi)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
