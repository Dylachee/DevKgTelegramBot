import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

# Функция для парсинга и сохранения данных
def parse_and_save():
    # Отправляем GET-запрос к странице
    url = 'https://devkg.com/ru/jobs'
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем HTML-код страницы
        html = response.text

        # Инициализация объекта BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Нахождение элементов с классом 'position-title' (названия категорий должностей)
        category_elements = soup.find_all('div', class_='jobs-item-field position')

        link_elements = soup.find_all('a', class_='link')

        # Создаем список словарей для хранения данных о категориях должностей и ссылках
        data = []
        
        # Извлекаем текст из элементов и сохраняем в список словарей
        for category_element, link_element in zip(category_elements, link_elements):
            category = category_element.text.strip()
            link = urljoin(url, link_element['href'])

            # Проверяем наличие ключевых слов в категории
            if 'junior' in category.lower() and 'python' in category.lower() and 'backend' in category.lower():
                data.append({'category': category, 'link': link})

        # Сохранение в JSON-файл
        with open('categories.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)

        print('Данные успешно сохранены в categories.json')
    else:
        print('Ошибка при получении страницы:', response.status_code)

# Бесконечный цикл для обновления страницы и записи данных каждые два часа
while True:
    parse_and_save()
    # Задержка на два часа (7200 секунд)
    time.sleep(7200)

