from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3
import requests
from config import token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

conn = sqlite3.connect('ojak_kebab.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY,
                   username TEXT,
                   first_name TEXT,
                   last_name TEXT,
                   date_joined DATE)''')
conn.commit()

class OrderFoodStates(StatesGroup):
    phone = State()
    address = State()

def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот оjak kebap. Какую информацию вы хотите получить?",
                        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                            types.KeyboardButton("Меню"),
                            types.KeyboardButton("О нас"),
                            types.KeyboardButton("Адрес"),
                            types.KeyboardButton("Заказать еду")
                        ))

@dp.message_handler(lambda message: message.text.strip() == "Меню")
async def send_menu(message: types.Message):
    address = """
 Меню  Ocak Kebap
Турецкий завтрак на 4 человека

Завтрак для одного человека

Завтрак турецкий на 2 человека

Менемен

Омлет с сыром"""
    await message.reply(address)

@dp.message_handler(lambda message: message.text.strip() == "О нас")
async def send_address(message: types.Message):
    address = """
Ocak Kebap
Кафе "Ожак Кебап" на протяжении 18 лет радует своих гостей изысканными турецкими блюдами в особенности своим кебабом.

Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.

В 2016 году по голосованию на сайте "Horeca" были удостоены "Лучшее кафе на каждый день" и мы стараемся оправдать доверие наших гостей.

Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е».
 У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции. Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков."""
    await message.reply(address)

@dp.message_handler(lambda message: message.text.strip() == "Адрес")
async def send_address(message: types.Message):
    address = "Адрес: улица Пр. Чуй 215/2, Бишкек, Кыргызстан"
    await message.reply(address)

@dp.message_handler(lambda message: message.text.strip() == "Заказать еду")
async def order_food(message: types.Message):
    await message.reply("Для заказа еды, пожалуйста, введите ваше имя:")
    await OrderFoodStates.phone.set()

@dp.message_handler(state=OrderFoodStates.phone)
async def process_name_step(message: types.Message, state: FSMContext):
    name = message.text
    users_data = {
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "date_joined": message.date
    }
    cursor.execute('''INSERT INTO users (username, first_name, last_name, date_joined) 
                      VALUES (?, ?, ?, ?)''', (users_data["username"], users_data["first_name"],
                                               users_data["last_name"], users_data["date_joined"]))
    conn.commit()
    await message.reply("Теперь введите ваш номер телефона:")
    await OrderFoodStates.next()



@dp.message_handler(state=OrderFoodStates.phone)
async def process_phone_step(message: types.Message, state: FSMContext):
    phone = message.text
    await message.reply("Теперь введите ваш адрес доставки:")
    await OrderFoodStates.next()
@dp.message_handler(state=OrderFoodStates.address)
async def process_address_step(message: types.Message, state: FSMContext):
    address = message.text
    await message.reply("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.")
    await state.finish()

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Извините, я не понимаю ваш запрос.")

executor.start_polling(dp, skip_updates=True)
