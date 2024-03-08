import logging
import random
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, Location
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

inline_start_buttons =[
    types.InlineKeyboardButton('Получить локацию', callback_data='get_location'),
    types.InlineKeyboardButton('Наш сайт', url='https://geeks.kg/')
]

inline_start_keyboard = types.InlineKeyboardMarkup().add(*inline_start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}",
    reply_markup=inline_start_keyboard)

@dp.message_handler(commands=['get_location'])
async def send_random_location(callback: types.CallbackQuery): 
    # Генерация случайных координат (широта и долгота)
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)

    # Отправка локации
    # await bot.send_location(message.chat.id, latitude, longitude)
    await callback.message.answer("Отправляю местоположение...") 
    await callback.message.answer_location(longitude=longitude, latitude=latitude)
    await callback.message.answer(f"{latitude}, {longitude}", 
    reply_markup=inline_start_keyboard)

executor.start_polling(dp, skip_updates=True)