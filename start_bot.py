from aiogram import Bot, Dispatcher, types, executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start') 
async def start(message:types.Message): 
    await message.answer("Привет Мир! hello geeks!") 
          
@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("Чем я могу вам помочь?")

@dp.message_handler(text="Geeks")
async def geeks(message:types.Message):
    await message.reply("Geeks - это айти курсы в Кыргызстане")

@dp.message_handler(text="hello")
async def hello(message:types.Message):
    await message.reply("Привет, как дела?")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    await message.answer_photo('https://th.bing.com/th/id/R.3a2cd96dce88505e89b69962a776cb6f?rik=bPwVOqQoC7KTHQ&riu=http%3a%2f%2fwww.hdcarwallpapers.com%2fwalls%2fmercedes_benz_g_63_amg-HD.jpg&ehk=TPjVGR8GNxD3kqi9jmZQLUeeTnPdubzPNuC1aa7yacE%3d&risl=&pid=ImgRaw&r=0')
    await message.answer_location(40.51936, 72.8027)
    await message.answer_photo()

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял, введите /help")

executor.start_polling(dp)




