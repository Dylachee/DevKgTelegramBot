from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor

# Создаем экземпляр бота
bot = Bot(token='6253951327:AAHecS-_Y3ujGss7nQ6Xzwt2Ft06QbyjJTs')
# Создаем диспетчер для обработки команд и сообщений
dispatcher = Dispatcher(bot, storage=MemoryStorage())

# Обработчик команды /start
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, который перенаправляет сообщения по тегам.")

# Обработчик всех входящих сообщений в группе
@dispatcher.message_handler(content_types=types.ContentType.TEXT, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def handle_message(message: types.Message):
    text = message.text
    chat_id = message.chat.id

    if 'Backend Python Junior' in text:
        # Перенаправляем сообщение в ваш личный чат с ботом
        await bot.forward_message(chat_id='1359779239', from_chat_id=chat_id, message_id=message.message_id)

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dispatcher)
