m, [14.02.2024 19:28]
from aiogram import Bot, Dispatcher,executor,types
from logging import basicConfig, INFO
from config import *
import sqlite3,uuid,time,os
from aiogram.types import *
from aiogram.types import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

storeg = MemoryStorage()
connection = sqlite3.connect('client.db')
cursor = connection.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users(
               id INT,
               username VARCHAR(200),
               first_name VARCHAR(200),
               last_name VARCHAR(200),
               cread VARCHAR(200)
               );""")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS receipt(
                    payment_code int, 
                    first_name VARCHAR(200),
                    last_name VARCHAR(200),
                    direction VARCHAR(200),
                    amount VARCHAR(200),
                    date VARCHAR(200)
                    );
                    """)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storeg)
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton('o нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Контакты'),
    types.KeyboardButton('Курсы'),
    
]
sk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    cursor.execute("SELECT * FROM users WHERE username = ?", (message.from_user.username,))
    existing_user = cursor.fetchone()
    if existing_user is None:
        cursor.execute("INSERT INTO users (id,username, first_name, last_name, cread) VALUES (?, ?, ?, ?, ?);",
                   (message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, time.ctime()))
    connection.commit()
    await message.answer("Привет, добро пожаловать в курсы Geeks", reply_markup=sk)
    
    connection.commit()

@dp.message_handler(text=['o нас'])
async def send_onas(message:types.Message):
    await message.reply('Geeks это айти курсы в Бишкеке, Карабалте и Оше созданы в 2019')
 

@dp.message_handler(text=['Адрес'])
async def send_фдрес(message:types.Message):
    await message.reply('Наш адрес \nMырзалды Аматова 1B (БЙ темирис)')  
    await message.answer_location(40.51962150364045, 72.80315285125309) 
    
    
@dp.message_handler(text=['Контакты'])
async def send_kantek(message:types.Message):
    await message.reply('наши контакты')
    await message.reply_contact("+996500102907", 'Aman', 'Omurzakov')

cb = [
    types.KeyboardButton('Backent'),
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Android'), 
    types.KeyboardButton('Назад')
   
]
ck = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*cb)



@dp.message_handler(text=['Курсы'])
async def send_kyrs(message:types.Message):
    await message.reply('Наши курсы',reply_markup=ck)
    
    
    
@dp.message_handler(text=['Назад'])
async def send_nazad(message:types.Message):
    await start(message)
    
class ReceiptState(StatesGroup):
    first_name = State()
    last_name = State()
    direction = State()
    amount = State()
    
@dp.message_handler(text=['Backent'])
async def beck(messege:types.Message):
    await messege.answer("Backent - это серверная сторона сайта которую мы не видем ")
 
@dp.message_handler(text=['Frontend'])
async def Frontend(messege:types.Message):
    await messege.answer("Frontend - это лицевая часть сайта которую мы видем ")

m, [14.02.2024 19:28]
@dp.message_handler(text=['UX/UI'])
async def ux(messege:types.Message):
    await messege.answer("UX/UI - это дизайн сайта или приложение  ")
    
@dp.message_handler(text=['Android'])
async def Android(messege:types.Message):
    await messege.answer("Android - это популятрная оперецоная система которую используют многие комнапии ")
    
@dp.message_handler(commands='receipt')
async def not_floun(message:types.Message): 
    await message.answer('для генераси чека введите следуюшие данные \n (имя, фамилия, направление, cymma)')
    await message.answer('Введите имя')
    await ReceiptState.first_name.set()
    
@dp.message_handler(state=ReceiptState.first_name)
async def get_last_name(message:types.Message, state:FSMContext): 
    await state.update_data(first_name = message.text)
    await message.answer('Введите фамилию')
    await ReceiptState.last_name.set()
    
@dp.message_handler(state=ReceiptState.last_name)
async def direct(message:types.Message, state:FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('Введите направление')
    await ReceiptState.direction.set()
    
@dp.message_handler(state=ReceiptState.direction)
async def get_amaot(message:types.Message, state:FSMContext):
    await state.update_data(direction=message.text)
    await message.answer('Введите сумму опалаты')
    await ReceiptState.amount.set()
    
@dp.message_handler(state=ReceiptState.amount)
async def generate_receipt(message:types.Message, state:FSMContext):
    await state.update_data(amount=message.text)
    result = await storeg.get_data(user=message.from_user.id)
    generate_payment_code = int(str(uuid.uuid4().int)[:10])
    print(generate_payment_code)
    print(result)
    cursor.execute(f"""INSERT INTO receipt (payment_code, first_name, last_name, direction, amount, date)
                   VALUES (?, ?, ?, ?, ?, ?);""", 
                   (generate_payment_code, result['first_name'], result['last_name'],
                    result['direction'], result['amount'], time.ctime()))
    connection.commit()
    await message.answer("Данные успешно записаны в базу данных")
    await message.answer(f"""Чек об оплате курса {result['direction']}
    Имя: {result['first_name']}
    Фамилия: {result['last_name']}
    Код оплаты: {generate_payment_code}
    Дата {time.ctime()}""")
    await message.answer("Генерирую PDF файл...")
    pdf_filename = f"receipt_{generate_payment_code}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"Direction: {result['direction']}")
    c.drawString(100, 730, f"First Name: {result['first_name']}")
    c.drawString(100, 710, f"Last Name: {result['last_name']}")
    c.drawString(100, 690, f"Payment Code: {generate_payment_code}")
    c.drawString(100, 670, f"Date: {time.ctime()}")
    c.save()

    await message.answer("PDF файл с чеком успешно сгенерирован")

    # Отправка PDF-файла пользователю
    with open(pdf_filename, 'rb') as pdf_file:
        await message.answer_document(pdf_file)
    await bot.send_message(-4037053389,f"""Чек об оплате курса {result['direction']}
Имя: {result['first_name']}
Фамилия: {result['last_name']}
Код оплаты: {generate_payment_code}
Дата: {time.ctime()}""")
    
    # Удаление временного PDF-файла
    os.remove(pdf_filename)
@dp.message_handler()
async def echo(message:types.Message):
    await message.answer('я не понел')    
    

executor.start_polling(dp)