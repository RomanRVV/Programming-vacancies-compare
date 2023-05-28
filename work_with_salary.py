
def predict_salary(salary_from, salary_to):
    if not salary_from:
        return salary_to * 0.8
    elif not salary_to:
        return salary_from * 1.2
    else:
        return salary_from + salary_to / 2


def predict_rub_salary_hh(vacancy):
    salary_info = vacancy['salary']
    salary = predict_salary(salary_info['from'], salary_info['to'])
    if not salary_info['currency'] == 'RUR':
        return None
    else:
        return salary


def predict_rub_salary_sj(vacancy):
    salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
    if not vacancy['currency'] == 'rub':
        return None
    elif salary == 0:
        return None
    else:
        return salary
