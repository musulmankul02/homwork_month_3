from aiogram import Bot, Dispatcher, types, executor
import logging, aioschedule, asyncio, requests
from datetime import datetime
from config import token 

bot = Bot(token = token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет!")
    
      
async def get_btc_price(chat_id):
    url= 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    btc_price = round(float(response.get('price')))
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await bot.send_message(chat_id, f'Цена биткоина: {btc_price} USD\nВремя: {current_time}')

async def scheduler(chat_id):
    aioschedule.every(5).seconds.do(get_btc_price, chat_id)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(parameter):
    chat_id= -4000645080
    asyncio.create_task(scheduler(chat_id))

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)