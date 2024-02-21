from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token
import logging, sqlite3, time

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

#Реализация Базы Данных на sqlite3
connection = sqlite3.connect('itbot.db')
cursor = connection.cursor()
cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    date_joined VARCHAR(100)
);
""")

start_keyboard = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Курсы'),
    types.KeyboardButton('Заявка на курсы')
]
start_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboard)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    print(message)
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    output_cursor = cursor.fetchall()
    print(output_cursor)
    if output_cursor ==[]:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (
            message.from_user.id, message.from_user.first_name,
            message.from_user.last_name, message.from_user.username, time.ctime()
        ))
        cursor.connection.commit()
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=start_button)
class Mallingstate(StatesGroup):
    text = State()

@dp.message_handler(text="Рассылка")
async def start_mailing(message:types.Message):
    await message.answer("Введите свой текст для рассылки; ")
    await Mallingstate.text.set()

@dp.message_handler(state=Mallingstate.text)
async def send_mailing(message:types.Message, state:FSMContext):
    await message.reply("Начинаю рассылку...")
    cursor.execute("SELECT id FROM users;")
    ali_users_ids = cursor.fetchall()
    print(ali_users_ids)
    for user_id in ali_users_ids:
        await bot.send_message(user_id[0], message.text)
    await message.answer("Рассылка окончена")
    await state.finish()

@dp.message_handler(text='О нас')
async def about_us(message:types.Message):
    await message.reply("Geeks - это айти курсы в Бишкеке, Кара-Балте, Оше и в Ташкенте!")

@dp.message_handler(text="Адрес")
async def send_address(message:types.Message):
    await message.answer("Наш адрес: Мырзалы Аматова 1Б (БЦ Томирис)")
    await message.answer_location(40.51936, 72.8027)

courses_keyboards = [
    types.KeyboardButton('Backend'),
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('iOS'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Назад'),
]
courses_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_keyboards)

@dp.message_handler(text="Курсы")
async def send_courses(message:types.Message):
    await message.answer("Вот наши курсы:", reply_markup=courses_button)

@dp.message_handler(text="Backend")
async def backend(message:types.Message):
    await message.reply("Backend - это внутреняя часть сайта или приложения.\nСрок обучения 5 месяцев\nСтоимость: 10000 KGS в месяц")

@dp.message_handler(text="Назад")
async def backroll(message:types.Message):
    await start(message)

executor.start_polling(dp)