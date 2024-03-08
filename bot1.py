import random, logging
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ParseMode
import geopandas as gpd
from shapely.geometry import Point
from config import token

logging.basicConfig(level=logging.INFO)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
land = world[world['continent'] != 'Antarctica']
land_bounds = land.geometry.bounds

bot = Bot(token=token)
dp = Dispatcher(bot)

inline_start_buttons =[
    types.InlineKeyboardButton('Получить локацию', callback_data='get_location'),
    types.InlineKeyboardButton('Наш сайт', url='https://geeks.kg/')
]

inline_start_keyboard = types.InlineKeyboardMarkup().add(*inline_start_buttons)

def generate_random_coordinates():
    while True:
        latitude = random.uniform(land_bounds['miny'].iloc[0], land_bounds['maxy'].iloc[0])
        longitude = random.uniform(land_bounds['minx'].iloc[0], land_bounds['maxx'].iloc[0])
        point = Point(float(longitude), float(latitude))  

        if land.geometry.contains(point).any():
            return latitude, longitude

@dp.message_handler(commands=['send_point'])
async def send_random_point(callback: types.CallbackQuery):
    latitude, longitude = generate_random_coordinates()
    await callback.message.answer_location(longitude=longitude, latitude=latitude)
    await callback.message.answer_location(f" {latitude} {longitude}",reply_markup=inline_start_keyboard)

executor.start_polling(dp, skip_updates=True)                                                                        