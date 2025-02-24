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
dp.callback_query_handler(text='add_user')(handlers.Admin.add_user)
dp.message_handler(state=handlers.Admin.Users.user)(handlers.Admin.add_user_phone)
dp.message_handler(state=handlers.Admin.Users.phone)(handlers.Admin.send_user)
dp.message_handler()(handlers.Start.hi)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)