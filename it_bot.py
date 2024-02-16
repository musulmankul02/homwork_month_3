from aiogram import Bot, Dispatcher, types, executor
from config import token 
import logging

bot = Bot(token = token)
dp = Dispatcher(bot)
logging.basicConfig(level = logging.INFO)

start_keyboard = [
    types.KeyboardButton("o нас"),
    types.KeyboardButton("адрес"),
    types.KeyboardButton("Курсы"),
    types.KeyboardButton("заявка на курсы")
]
start_botton = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboard)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    print(message)
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=start_botton)

@dp.message_handler(text="o нас")
async def about_us(message:types.Message):
    await message.answer("Geeks - ")

@dp.message_handler(text='адрес')
async def send_address(message:types.Message):
    await message.answer("Нащ адрес: Мырзалы Аматова 1Б (БЦ Томирис) ")
    await message.answer_location(40.51936, 72.8027)


keybordcourses = [
    types.KeyboardButton("Bakend"),
    types.KeyboardButton("Frontend"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("Назад")
]
courses = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*keybordcourses)

@dp.message_handler(text='Курсы')
async def start(message:types.Message):
    print(message)
    await message.answer(f"Привет {message.from_user.full_name}",  reply_markup=courses)

@dp.message_handler(text = 'Bakend')
async def Bakend(message:types.Message):
    await message.answer("Backent - это серверная сторона сайта которую мы не видем ")

@dp.message_handler(text = 'Frontend')
async def fronten(message:types.Message):
    await message.answer("Frontend - это лицевая часть сайта которую мы видем ")

@dp.message_handler(text='UX/UI')
async def ux(messege:types.Message):
    await messege.answer("UX/UI - это дизайн сайта или приложение  ")

@dp.message_handler(text = 'Android')
async def androud(messsage:types.Message):
    await messsage.answer("Android - это популятрная оперецоная система которую используют многие комнапииAndroid - ")

@dp.message_handler(text='Назад')
async def send_nazad(message:types.Message):
    await start(message)
    
executor.start_polling(dp)

