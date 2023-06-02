
def predict_salary(salary_from, salary_to):
    if not salary_from:
        return salary_to * 0.8
    elif not salary_to:
        return salary_from * 1.2
    else:
        return salary_from + salary_to / 2


def predict_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    try:
        average_salary = predict_salary(salary['from'], salary['to'])
    except TypeError:
        return None
    if not salary['currency'] == 'RUR':
        return None
    else:
        return average_salary


def predict_rub_salary_sj(vacancy):
    salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
    if not vacancy['currency'] == 'rub' or not salary:
        return None
    else:
        return salary
