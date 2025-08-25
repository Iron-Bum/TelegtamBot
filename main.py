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
import handlers.Start
import handlers.Admin
import database

api = config.API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.message_handler(commands=['admin'])(handlers.Admin.start)
dp.callback_query_handler(text=['choice_yes', 'choice_nou'], state=handlers.Admin.ServiceState.name)(handlers.Admin.hendl_choice)
dp.message_handler(Text(equals=['Добавить клиента']))(handlers.Admin.add_user)
dp.message_handler(Text(equals=['Добавить (редактировать) услугу']))(handlers.Admin.add_service)
dp.message_handler(Text(equals=['Получить ID']))(handlers.Admin.get_client_id_step_1)
dp.message_handler(Text(equals=['Добавить мастера']))(handlers.Admin.add_master)
dp.message_handler(Text(equals=['Запись']))(handlers.Admin.start_choice_date)
dp.message_handler(state=handlers.Admin.UserState.user_id)(handlers.Admin.get_client_id_step_2)
dp.message_handler(state=handlers.Admin.MasterState.name)(handlers.Admin.send_master)
dp.message_handler(state=handlers.Admin.UserState.name)(handlers.Admin.add_user_phone)
dp.message_handler(state=handlers.Admin.UserState.phone)(handlers.Admin.send_user)
dp.message_handler(state=handlers.Admin.ServiceState.name)(handlers.Admin.add_service_price)
dp.message_handler(state=handlers.Admin.ServiceState.cost)(handlers.Admin.send_service)
dp.message_handler(state=handlers.Admin.BookingState.choosing_date)(handlers.Admin.week_navigation_handler)
dp.message_handler(state=handlers.Admin.BookingState.choosing_time)(handlers.Admin.day_navigation_handler)
dp.message_handler()(handlers.Start.hi)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)