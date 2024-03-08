import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
import geopandas as gpd
from shapely.geometry import Point
from config import token

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

land = world[world['continent'] != 'Antarctica']

land_bounds = land.geometry.bounds

bot = Bot(token=token)
dp = Dispatcher(bot)

def generate_random_coordinates():
    while True:
        latitude = random.uniform(land_bounds['miny'].iloc[0], land_bounds['maxy'].iloc[0])
        longitude = random.uniform(land_bounds['minx'].iloc[0], land_bounds['maxx'].iloc[0])
        point = Point(float(longitude), float(latitude))  

        if land.geometry.contains(point).any():
            return latitude, longitude

@dp.message_handler(commands=['send_point'])
async def send_random_point(message: types.Message):
    latitude, longitude = generate_random_coordinates()
    await message.reply(f"Случайная точка на суше:\nШирота: {latitude}\nДолгота: {longitude}")

executor.start_polling(dp, skip_updates=True)  