import sys
import os
sys.path.append(os.path.join(os.getcwd(),'..'))


async def hi(message):
    await message.answer('Введите команду /start, что бы начть общение')