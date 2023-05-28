import requests
from itertools import count
import time
import json
from dotenv import load_dotenv, find_dotenv
import os

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
    vacancy = []
    for page in count(0):
        payload = {
            'professional_role': 96,
            'per_page': 20,
            'page': page,
            'area': 1,
            'period': 30,
            'text': language,
            'only_with_salary': True
        }

        try:
            page_response = requests.get(url, params=payload)
            page_response.raise_for_status()
            page_payload = page_response.json()
            vacancy.append(page_payload)
            print(page, page_payload['pages'], payload['text'])
            if page >= page_payload['pages']:
                break

        except requests.exceptions.HTTPError:
            print('Введите капчу')
            print(page_response.json()['errors'][0]['captcha_url'] + '&backurl')
            time.sleep(int(input('Скачивание продолжится через: ')))
    return vacancy


def fetch_records_sj(language):
    load_dotenv(find_dotenv())
    superjob_key = os.environ['SUPERJOB_KEY']

    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': superjob_key
    }
    vacancy = []
    for page in count(0):
        payload = {
            'town': 4,
            'catalogues': 48,
            'keyword': language,
            'page': page,
            'count': 100
        }

        page_response = requests.get(url, params=payload, headers=headers)
        page_response.raise_for_status()
        page_payload = page_response.json()
        vacancy.append(page_payload)
        print(page, page_payload['more'], payload['keyword'])
        if not page_payload['more']:
            break

    return vacancy


def main():
    vacancy_hh = {}
    vacancy_sj = {}
    for language in programming_languages:
        vacancy_hh[language] = fetch_records_hh(language)
        vacancy_sj[language] = fetch_records_sj(language)
    with open('hh_records.json', 'w', encoding='utf-8') as f:
        json.dump(vacancy_hh, f, indent=2, ensure_ascii=False)
    with open('sj_records.json', 'w', encoding='utf-8') as f:
        json.dump(vacancy_sj, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
