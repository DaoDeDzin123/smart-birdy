import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from model import get_address
from arq import create_pool, Worker
from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings(host="localhost", port=6379)

TOKEN = "TOKEN"
CHAT_ID = 123

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def message_start(message: types.Message):
    await message.answer("Вас приветствует Smart Birdy!")

async def new_photo(ctx, id):
    photo_address = await get_address(id)
    photo_address =  "../smart-birdy/" + photo_address
    photo = types.FSInputFile(photo_address)
    await bot.send_photo(chat_id=CHAT_ID, photo=photo)

async def startup(ctx):
    ctx["redis"] = await  create_pool(REDIS_SETTINGS)

async def shutdown(ctx):
    await ctx["redis"].close()

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

class WorkerSettings:
    functions = [new_photo]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = REDIS_SETTINGS



try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.info("Бот остановлен")



