import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from model import get_address
import redis

TOKEN = "TOKEN"
CHAT_ID = 123

redis_conn = redis.Redis(decode_responses=True)
queue_name = "queue"

def get_task():
    item = redis_conn.brpop([queue_name], timeout=1)
    if item is not None:
        res = item[1]
        return int(res)
    return None

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def message_start(message: types.Message):
    await message.answer("Вас приветствует Smart Birdy!")

async def new_photo(id):
    photo_address = await get_address(id)
    photo_address =  "../smart-birdy/" + photo_address
    photo = types.FSInputFile(photo_address)
    await bot.send_photo(chat_id=CHAT_ID, photo=photo)

async def main():
    try:
        await dp.start_polling(bot)
        while True:
            task = get_task()
            if task is not None:
                await new_photo(task)
    finally:
        await bot.session.close()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.info("Бот остановлен")



