import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

def parse_and_save():
    url = 'https://devkg.com/ru/jobs'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        category_elements = soup.find_all('div', class_='jobs-item-field position')
        link_elements = soup.find_all('a', class_='link')

        data = []

        for category_element, link_element in zip(category_elements, link_elements):
            category = category_element.text.strip()
            link = urljoin(url, link_element['href'])

            if 'junior' in category.lower() and 'python' in category.lower() and 'backend' in category.lower():
                # Создаем словарь с основными данными
                job_data = {'category': category, 'link': link}

                # Отправляем GET-запрос к странице работодателя
                employer_response = requests.get(link)
                if employer_response.status_code == 200:
                    employer_html = employer_response.text
                    employer_soup = BeautifulSoup(employer_html, 'html.parser')

                    # Извлекаем данные о работодателе
                    information = employer_soup.find('main', class_='job-body').text.strip()
                    owner_element = employer_soup.find('div', class_='organizations-item-field name')
                    owner = owner_element.text.strip() if owner_element else None

                    # Добавляем данные о работодателе в словарь

                    job_data['information'] = information
                    job_data['owner'] = owner
                data.append(job_data)

        with open('WithFilter/categories.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)

        print('Данные успешно сохранены')
    else:
        print('Ошибка при получении страницы:', response.status_code)

while True:
    parse_and_save()
    time.sleep(7200)
