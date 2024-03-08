from aiogram import Bot, Dispatcher, types, executor
from config import token 
import logging, aioschedule, asyncio

bot = Bot(token = token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет!")
    
async def send_message():
    await bot.send_message(-4000645080,"Привет всем!")
    
async def scheduler():
    aioschedule.every(5).seconds.do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(parameter):
    asyncio.create_task(scheduler())
    
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
