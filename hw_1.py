import random 
from aiogram import Bot, Dispatcher, types, executor 
from config import token 
 
 
bot = Bot(token=token) 
dp = Dispatcher(bot) 
 
@dp.message_handler(commands='start') 
async def start(message: types.Message): 
    await message.reply("Привет! Я загадал число от 1 до 3. Попробуйте угадать!") 
 
@dp.message_handler(lambda message: message.text) 
async def guess_number(message: types.Message): 
    user_guess = int(message.text) 
    bot_number = random.randint(1, 3) 

    if user_guess == bot_number: 
        await message.answer("вы победили!") 
        await message.answer_photo("https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg") 
         
    else: 
        await message.answer(f"Вы не угадали число. Бот загадал число {bot_number}") 
        await message.answer_photo("https://media.makeameme.org/created/sorry-you-lose.jpg") 

executor.start_polling(dp)