import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor

# Создаем экземпляр бота
bot = Bot(token='6253951327:AAHecS-_Y3ujGss7nQ6Xzwt2Ft06QbyjJTs')
# Создаем диспетчер для обработки команд и сообщений
dispatcher = Dispatcher(bot, storage=MemoryStorage())

# Загружаем данные из файла categories.json
def load_categories():
    with open('categories.json', 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

# Обработчик команды /start
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, который отправляет данные из файла categories.json.")

# Обработчик команды /show
@dispatcher.message_handler(commands=['show'])
async def show_categories(message: types.Message):
    data = load_categories()
    if data:
        for item in data:
            category = item['category']
            link = item['link']
            await message.answer(f"Категория: {category}\nСсылка: {link}")
    else:
        await message.answer("Нет доступных категорий.")

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
