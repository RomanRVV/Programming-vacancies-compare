from fetch_records import programming_languages, fetch_records_sj, fetch_records_hh
from work_with_salary import predict_rub_salary_hh, predict_rub_salary_sj
from terminaltables import AsciiTable
import argparse


def hh_average_salary_sorted_by_language(vacancies, language):
    vacancies_number = {}
    salaries = []
    for vacancies_info in vacancies:
        for vacancy_info in vacancies_info['items']:
            salary = predict_rub_salary_hh(vacancy_info)
            if not salary:
                continue
            else:
                salaries.append(salary)

        average_salary = sum(salaries) / len(salaries)

        vacancies_number.update({
            language: {
                "average_salary": int(average_salary),
                "vacancies_processed": len(salaries),
                "vacancies_found": vacancies_info['found']
            }
        })
    return vacancies_number


def sj_average_salary_sorted_by_language(vacancies, language):
    vacancies_number = {}
    salaries = []
    for vacancies_info in vacancies:
        for vacancy_info in vacancies_info['objects']:
            salary = predict_rub_salary_sj(vacancy_info)
            if not salary:
                continue
            else:
                salaries.append(salary)
        try:
            average_salary = sum(salaries) / len(salaries)
            vacancies_number.update({
                language: {
                    "average_salary": int(average_salary),
                    "vacancies_processed": len(salaries),
                    "vacancies_found": vacancies_info['total']
                }
            })
        except ZeroDivisionError:
            vacancies_number.update({
                language: {
                    "average_salary": 'Нет результатов',
                    "vacancies_processed": 'Нет результатов',
                    "vacancies_found": 'Нет результатов'
                }
            })
    return vacancies_number


def salary_table_created_sj(salary_statistics):
    title = 'SuperJob Moscow'
    table_data = [
        ['Язык программирования', ' Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for count, salary_info in enumerate(salary_statistics):
        language = [*salary_info.keys()]
        table_data.append([*salary_info.keys(),
                           salary_statistics[count][f'{language[0]}']['vacancies_found'],
                           salary_statistics[count][f'{language[0]}']['vacancies_processed'],
                           salary_statistics[count][f'{language[0]}']['average_salary']]
                          )
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def salary_table_created_hh(salary_statistics):
    title = 'HeadHunter Moscow'
    table_data = [
        ['Язык программирования', ' Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for count, salary_info in enumerate(salary_statistics):
        language = [*salary_info.keys()]
        table_data.append([*salary_info.keys(),
                           salary_statistics[count][f'{language[0]}']['vacancies_found'],
                           salary_statistics[count][f'{language[0]}']['vacancies_processed'],
                           salary_statistics[count][f'{language[0]}']['average_salary']]
                          )
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def main():
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
        vacancy_sj[language] = fetch_records_sj(language)
        vacancies_sj.append(sj_average_salary_sorted_by_language(vacancy_sj[language], language))
        vacancies_hh.append(hh_average_salary_sorted_by_language(vacancy_hh[language], language))

    print(salary_table_created_sj(vacancies_sj))
    print(salary_table_created_hh(vacancies_hh))


if __name__ == '__main__':
    main()
