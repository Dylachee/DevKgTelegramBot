import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot('6293863481:AAFTWjUAGFXMne006tGeSGuzlTLAMbhGy_w')  # Укажите свой токен бота
dp = Dispatcher(bot)

# Чтение данных из JSON-файла
with open('jobs.json', 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

# Создание списка схожих результатов
similar_results = []

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text='Frontend', callback_data='frontend')
    button1 = types.InlineKeyboardButton(text='.NET', callback_data='.NET')
    button2 = types.InlineKeyboardButton(text='Middle/Senior', callback_data='Middle/Senior')
    button3 = types.InlineKeyboardButton(text='Mobile', callback_data='Mobile')
    button4 = types.InlineKeyboardButton(text='Flutter', callback_data='Flutter')
    markup.add(button, button1, button2, button3, button4)
    await message.reply('Выберите категорию:', reply_markup=markup)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'frontend')
async def frontend_callback(callback_query: types.CallbackQuery):
    global similar_results
    similar_results = []
    for job in data:
        if 'frontend' in job['category'].lower():
            similar_results.append(job)
    await callback_query.answer('Вы выбрали категорию "Frontend"')
    await search_jobs(callback_query.message)

@dp.callback_query_handler(lambda callback_query: callback_query.data == '.NET')
async def frontend_callback(callback_query: types.CallbackQuery):
    global similar_results
    similar_results = []
    for job in data:
        if '.net' in job['category'].lower():
            similar_results.append(job)
    await callback_query.answer('Вы выбрали категорию ".NET"')
    await search_jobs(callback_query.message)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'Middle/Senior')
async def frontend_callback(callback_query: types.CallbackQuery):
    global similar_results
    similar_results = []
    for job in data:
        if 'middle/senior' in job['category'].lower():
            similar_results.append(job)
    await callback_query.answer('Вы выбрали категорию "Middle/Senior"')
    await search_jobs(callback_query.message)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'Mobile')
async def frontend_callback(callback_query: types.CallbackQuery):
    global similar_results
    similar_results = []
    for job in data:
        if 'mobile' in job['category'].lower():
            similar_results.append(job)
    await callback_query.answer('Вы выбрали категорию "Mobile"')
    await search_jobs(callback_query.message)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'Flutter')
async def frontend_callback(callback_query: types.CallbackQuery):
    global similar_results
    similar_results = []
    for job in data:
        if 'flutter' in job['category'].lower():
            similar_results.append(job)
    await callback_query.answer('Вы выбрали категорию "Flutter"')
    await search_jobs(callback_query.message)

@dp.message_handler()
async def search_jobs(message: types.Message):
    if similar_results:
        for job in similar_results:
            job_text = f"{job['category']}\n{job['link']}\n\n{job['information']}"
            await message.answer(job_text)

            # Добавляем кнопку "Фильтры" после каждого сообщения
            filters_button = types.InlineKeyboardButton(text='Фильтры', callback_data='filters')
            markup = types.InlineKeyboardMarkup().add(filters_button)
            await message.answer('Выберите фильтры:', reply_markup=markup)
    else:
        await message.answer('Ничего не найдено')

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'filters')
async def filters_callback(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text='Frontend', callback_data='frontend')
    button1 = types.InlineKeyboardButton(text='.NET', callback_data='.NET')
    button2 = types.InlineKeyboardButton(text='Middle/Senior', callback_data='Middle/Senior')
    button3 = types.InlineKeyboardButton(text='Mobile', callback_data='Mobile')
    button4 = types.InlineKeyboardButton(text='Flutter', callback_data='Flutter')
    markup.add(button, button1, button2, button3, button4)
    await callback_query.message.answer('Выберите категорию:', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

