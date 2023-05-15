import json
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot('YOUR_TOKKEN')  # Укажите свой токен бота
dp = Dispatcher(bot)

# Чтение данных из JSON-файла
with open('WithoutFilter/jobs.json', 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

# Создание словаря тегов и подписок
tags_subscriptions = {}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text='Показать вакансии по фильтру', callback_data='show_jobs')
    markup.add(button)
    await message.reply('Выберите фильтр для вакансий:', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'show_jobs')
async def show_jobs_callback(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Frontend', callback_data='frontend')
    button2 = types.InlineKeyboardButton(text='.NET', callback_data='.NET')
    button3 = types.InlineKeyboardButton(text='Middle/Senior', callback_data='Middle/Senior')
    button4 = types.InlineKeyboardButton(text='Mobile', callback_data='Mobile')
    button5 = types.InlineKeyboardButton(text='Flutter', callback_data='Flutter')
    button6 = types.InlineKeyboardButton(text='Backend', callback_data='Backend')
    button7 = types.InlineKeyboardButton(text='Python', callback_data='Python')
    markup.add(button1, button2, button3, button4, button5,button6, button7)
    await callback_query.message.answer('Выберите теги для фильтрации вакансий:', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data in ['frontend', '.NET', 'Middle/Senior', 'Mobile', 'Flutter', 'Backend','Python'])
async def tag_selection_callback(callback_query: types.CallbackQuery):
    tag = callback_query.data
    user_id = callback_query.from_user.id

    if tag in tags_subscriptions.get(user_id, []):
        tags_subscriptions[user_id].remove(tag)
        await callback_query.answer(f'Вы отписались от тега "{tag}"')
    else:
        tags_subscriptions.setdefault(user_id, []).append(tag)
        await callback_query.answer(f'Вы подписались на тег "{tag}"')

    markup = types.InlineKeyboardMarkup(row_width=1)
    subscribe_button = types.InlineKeyboardButton(text='Подписаться на уведомления', callback_data='subscribe')
    markup.add(subscribe_button)
    await callback_query.message.answer('Хотите подписаться на уведомления о новых вакансиях?', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'subscribe')
async def subscribe_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_subscriptions = tags_subscriptions.get(user_id, [])

    if user_subscriptions:
        await callback_query.answer('Вы успешно подписались на уведомления!')
        
        # Здесь вы можете добавить код для сохранения подписки пользователя, например, в базу данных
        
        await callback_query.message.delete()
        await send_job_notifications(user_id)  # Запуск задачи отправки уведомлений для пользователя
    else:
        await callback_query.answer('Для подписки на уведомления выберите хотя бы один тег!')


async def send_job_notifications(user_id: int):
    while True:
        user_subscriptions = tags_subscriptions.get(user_id, [])
        if user_subscriptions:
            for job in data:
                if any(tag.lower() in job['category'].lower() for tag in user_subscriptions):
                    job_text = f"{job['category']}\n{job['link']}\n\n{job['information']}"
                    await bot.send_message(chat_id=user_id, text=job_text)
        await asyncio.sleep(10)  # Пауза в 1 час (можете изменить по своему усмотрению)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)