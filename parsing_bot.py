from aiogram import Bot, Dispatcher, types, executor
from config import token
from bs4 import BeautifulSoup
import logging, requests

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def hello(message:types.Message):
    await message.answer("Привет, напиши /news для получения новостей")

@dp.message_handler(commands='news')
async def news(message:types.Message):
    await message.answer("Отпровляю новости ...")
    number_ner_news = 0
    for page in range(1,10):
        url = f'https://stopgame.ru/news/all/p1{page}/'
        respons = requests.get(url=url)
        # print(respons)
        soup = BeautifulSoup(respons.text, 'lxml')
        # print(soup)
        all_news = soup.find_all('a', class_='_title_11mk8_60')
        # print(all_news)
        for news in all_news:
            print(news.txt)
            number_ner_news += 1 
            # print(f"{number_news}) {news.text}")
            await message.answer(f'{number_ner_news}) {news.text}')

executor.start_polling(dp, skip_updates=True)