import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN

from scraping_parsing import extract
from sql_queries import connect_to_DB, disconnect_from_DB, execute_query



# Подключение к БД
connection = connect_to_DB()

logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет, этот бот позволяет узнать актуальные курсы драгоценных металлов и определить куда инвестировать \n\n Введи команду /get чтобы начать получать оповещения")


@dp.message(Command("get"))
async def get_info(message: Message):
    while True:
        metals = extract() # Извлечение данных о металлах с сайта

        # Внесение данных о металлах в БД
        execute_query(connection, query="INSERT INTO precious_metals (name, price_to_buy, price_to_sell) VALUES" \
                                       f"('Золото', {float((metals['gold']["Купить"]))}, {metals["gold"]["Продать"]})," \
                                       f"('Серебро', {float((metals['silver']["Купить"]))}, {metals["silver"]["Продать"]})," \
                                       f"('Платина', {float((metals['platinum']["Купить"]))}, {metals["platinum"]["Продать"]})," \
                                       f"('Палладий', {float((metals['palladium']["Купить"]))}, {metals["palladium"]["Продать"]});")

        await message.answer(f"Золото \n Купить: {metals["gold"]["Купить"]} (руб/г) \n Продать: {metals["gold"]["Продать"]} (руб/г) \n\n"
                             f"Серебро \n Купить: {metals["silver"]["Купить"]} (руб/г) \n Продать: {metals["silver"]["Продать"]} (руб/г)")
        await asyncio.sleep(1800)


# Основная функция
async def main():
    logger.info("Запуск бота...")
    
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
        disconnect_from_DB(connection, comment="Отключение от БД")