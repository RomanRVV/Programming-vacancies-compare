import requests
from itertools import count
import time

programming_languages = [
    'Python',
    'Java',
    'JavaScript',
    '1c',
    'PHP',
    'C++',
    'C#',
    '!C'
]


def fetch_records_hh(language):
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    moscow_id_hh = 1
    programmer_profession_id_hh = 96
    number_of_items_page = 100
    publication_date_limit = 30
    for page in count(0):
        payload = {
            'professional_role': programmer_profession_id_hh,
            'per_page': number_of_items_page,
            'page': page,
            'area': moscow_id_hh,
            'period': publication_date_limit,
            'text': language
        }
        try:
            page_response = requests.get(url, params=payload)
            page_response.raise_for_status()
            page_payload = page_response.json()
            vacancies.append(page_payload)
            if page >= page_payload['pages']:
                break
            elif page >= 19:
                break
        except requests.exceptions.HTTPError:

            print('Введите капчу')
            print(page_response.json()['errors'][0]['captcha_url'] + '&backurl')
            time.sleep(int(input('Скачивание продолжится через: ')))
    return vacancies


def fetch_records_sj(language, api_key):
    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': api_key
    }
    vacancies = []
    moscow_id_sj = 4
    programmer_profession_id_sj = 48
    number_of_items_page = 100
    for page in count(0):
        payload = {
            'town': moscow_id_sj,
            'catalogues': programmer_profession_id_sj,
            'keyword': language,
            'page': page,
            'count': number_of_items_page
        }

        page_response = requests.get(url, params=payload, headers=headers)
        page_response.raise_for_status()
        page_payload = page_response.json()
        vacancies.append(page_payload)
        if not page_payload['more']:
            break
    return vacancies
