from fetch_records import PROGRAMMING_LANGUAGES, fetch_vacancies_sj, fetch_vacancies_hh
from work_with_salary import predict_rub_salary_hh, predict_rub_salary_sj
from terminaltables import AsciiTable
from dotenv import load_dotenv, find_dotenv
import os


def get_salary_statistics_hh(vacancies):
    salary_statistics = {}
    salaries = []
    for vacancy in vacancies:
        for salary in vacancy['items']:
            average_salary = predict_rub_salary_hh(salary)
            if average_salary:
                salaries.append(average_salary)
    try:
        total_average_salary = sum(salaries) / len(salaries)
        salary_statistics.update({
                "average_salary": int(total_average_salary),
                "vacancies_processed": len(salaries),
                "vacancies_found": vacancy['found']
            })
    except ZeroDivisionError:
        salary_statistics.update({
            "average_salary": 'Нет результатов',
            "vacancies_processed": 'Нет результатов',
            "vacancies_found": vacancy['found']
         })
    return salary_statistics


def get_salary_statistics_sj(vacancies):
    salary_statistics = {}
    salaries = []
    for vacancy in vacancies:
        for salary in vacancy['objects']:
            average_salary = predict_rub_salary_sj(salary)
            if average_salary:
                salaries.append(average_salary)
    try:
        total_average_salary = sum(salaries) / len(salaries)
        salary_statistics.update({
                "average_salary": int(total_average_salary),
                "vacancies_processed": len(salaries),
                "vacancies_found": vacancy['total']
            })
    except ZeroDivisionError:
        salary_statistics.update({
                "average_salary": 'Нет результатов',
                "vacancies_processed": 'Нет результатов',
                "vacancies_found": vacancy['total']
            })
    return salary_statistics


def create_salary_table(salary_statistics, title):
    table = [
        ['Язык программирования', ' Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language, salary in salary_statistics.items():
        table.append([language,
                      salary['vacancies_found'],
                      salary['vacancies_processed'],
                      salary['average_salary']]
                     )
    table_instance = AsciiTable(table, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def main():
    load_dotenv(find_dotenv())
    superjob_key = os.environ['SUPERJOB_KEY']
    hh_vacancies = {}
    sj_vacancies = {}
    sj_salary_statistics = {}
    hh_salary_statistics = {}
    for language in PROGRAMMING_LANGUAGES:
        hh_vacancies[language] = fetch_vacancies_hh(language)
        sj_vacancies[language] = fetch_vacancies_sj(language, superjob_key)
        sj_salary_statistics[language] = get_salary_statistics_sj(sj_vacancies[language])
        hh_salary_statistics[language] = get_salary_statistics_hh(hh_vacancies[language])

    print(create_salary_table(sj_salary_statistics, 'SuperJob Moscow'))
    print(create_salary_table(hh_salary_statistics, 'HeadHunter Moscow'))


if __name__ == '__main__':
    main()
