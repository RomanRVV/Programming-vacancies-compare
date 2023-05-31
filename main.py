from fetch_records import programming_languages, fetch_records_sj, fetch_records_hh
from work_with_salary import predict_rub_salary_hh, predict_rub_salary_sj
from terminaltables import AsciiTable
import argparse
from dotenv import load_dotenv, find_dotenv
import os


def sort_average_salary_hh_by_language(vacancies, language):
    vacancies_number = {}
    salaries = []
    for vacancy in vacancies:
        for salary in vacancy['items']:
            average_salary = predict_rub_salary_hh(salary)
            if not average_salary:
                continue
            else:
                salaries.append(average_salary)
    total_average_salary = sum(salaries) / len(salaries)
    vacancies_number[language] = {
            "average_salary": int(total_average_salary),
            "vacancies_processed": len(salaries),
            "vacancies_found": vacancy['found']
        }
    return vacancies_number


def sort_average_salary_sj_by_language(vacancies, language):
    vacancies_number = {}
    salaries = []
    for vacancy in vacancies:
        for salary in vacancy['objects']:
            average_salary = predict_rub_salary_sj(salary)
            if not average_salary:
                continue
            else:
                salaries.append(average_salary)
    try:
        total_average_salary = sum(salaries) / len(salaries)
        vacancies_number[language] = {
                "average_salary": int(total_average_salary),
                "vacancies_processed": len(salaries),
                "vacancies_found": vacancy['total']
            }
    except ZeroDivisionError:
        vacancies_number[language] = {
                "average_salary": 'Нет результатов',
                "vacancies_processed": 'Нет результатов',
                "vacancies_found": 'Нет результатов'
            }
    return vacancies_number


def create_salary_table_sj(salary_statistics):
    title = 'SuperJob Moscow'
    table = [
        ['Язык программирования', ' Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for count, salary in enumerate(salary_statistics):
        language = [*salary.keys()]
        table.append([*salary.keys(),
                      salary_statistics[count][f'{language[0]}']['vacancies_found'],
                      salary_statistics[count][f'{language[0]}']['vacancies_processed'],
                      salary_statistics[count][f'{language[0]}']['average_salary']]
                     )
    table_instance = AsciiTable(table, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def create_salary_table_hh(salary_statistics):
    title = 'HeadHunter Moscow'
    table = [
        ['Язык программирования', ' Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for count, salary in enumerate(salary_statistics):
        language = [*salary.keys()]
        table.append([*salary.keys(),
                      salary_statistics[count][f'{language[0]}']['vacancies_found'],
                      salary_statistics[count][f'{language[0]}']['vacancies_processed'],
                      salary_statistics[count][f'{language[0]}']['average_salary']]
                     )
    table_instance = AsciiTable(table, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def main():
    load_dotenv(find_dotenv())
    superjob_key = os.environ['SUPERJOB_KEY']
    parser = argparse.ArgumentParser(
        description='Скачивает и выводит зарплатную статистику вакансий с сайтов SuperJob и HH'
    )
    parser.add_argument('--add_language', help='Добавить язык программирования для сбора статистики')
    args = parser.parse_args()
    if args.add_language:
        programming_languages.append(args.add_language)
    vacancy_hh = {}
    vacancy_sj = {}
    vacancies_sj = []
    vacancies_hh = []
    for language in programming_languages:
        vacancy_hh[language] = fetch_records_hh(language)
        vacancy_sj[language] = fetch_records_sj(language, superjob_key)
        vacancies_sj.append(sort_average_salary_sj_by_language(vacancy_sj[language], language))
        vacancies_hh.append(sort_average_salary_hh_by_language(vacancy_hh[language], language))

    print(create_salary_table_sj(vacancies_sj))
    print(create_salary_table_hh(vacancies_hh))


if __name__ == '__main__':
    main()
