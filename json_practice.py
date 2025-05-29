import random
import json

# Задача 1
def generate_users(first_names: list[str], last_names: list[str], cities:list[str]) -> dict:
    """Генерирует пользователя."""

    while True:
        user = {
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'age': random.randint(18, 65),
            'city': random.choice(cities)
        }
        yield user


if __name__ == '__main__':
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']
    first_names = ['John', 'Jane', 'Mark', 'Emily', 'Michael', 'Sarah']
    last_names = ['Doe', 'Smith', 'Johnson', 'Brown', 'Lee', 'Wilson']

    users = generate_users(first_names, last_names, cities)

    user_group1 = [next(users) for i in range(4)]
    user_group2 = [next(users) for i in range(6)]

    print('User group #1')
    print(json.dumps(user_group1, indent=4))
    print('User group #2')
    print(json.dumps(user_group2, indent=4))

# Задача 2

def stat_decorator(func):
    """Декоратор для вывода статистики по отфильтрованным транзакциям."""

    def wrapper(*args, **kwargs):
        filtered_transactions = func(*args, **kwargs)
        total_amount = sum([transaction['amount'] for transaction in filtered_transactions])
        print(f"Отфильтровано {len(filtered_transactions)} транзакций на сумму {total_amount}")
        return filtered_transactions

    return wrapper

@stat_decorator
def filter_transactions_by_currency(input_file, output_file, currency):
    """Фильтрует транзакции по валюте и сохраняет результат в новый файл."""

    with open(input_file, 'r') as f:
        transactions = json.load(f)

    filtered_transactions = [transaction for transaction in transactions if transaction['currency'] == currency]

    with open(output_file, 'w') as f:
        json.dump(filtered_transactions, f, indent=4)

    return filtered_transactions

def main():
    input_file = 'transactions.json'
    output_file = 'transactions_filtered.json'
    currency = 'USD'

    filtered_transactions = filter_transactions_by_currency(input_file, output_file, currency)
    print(filtered_transactions)

if __name__ == '__main__':
    main()

# Задача 3
import json

import requests

def get_github_users(users):
    results = []
    for user in users:
        status, user_data = get_user_info(user)
        if not status:
            continue

        status, repositories = get_user_repos(user)
        if not status:
            continue

        result = {
            'login': user_data['login'],
            'public_repos': user_data['public_repos'],
            'repositories': repositories
        }
        results.append(result)
    return json.dumps(results)

def get_user_info(user: str) -> tuple[bool, dict]:
    url = f"https://api.github.com/users/{user}"
    response = requests.get(url)
    if response.status_code != 200:
        return False, {}
    return True, response.json()

def get_user_repos(user: str) -> tuple[bool, list]:
    repo_url = f"https://api.github.com/users/{user}/repos"
    repo_response = requests.get(repo_url)
    if repo_response.status_code != 200:
        return False, []
    return True, [repo['name'] for repo in repo_response.json()]



# Задача 4
# Напишите функцию, которая будет получать курс валюты на текущую дату из API ЦБ РФ и возвращать его в формате JSON.
# Используйте сайт https://www.cbr-xml-daily.ru/daily_json.js.
# Пример вызова функции:
# rate = get_currency_rate("USD")
# print(rate)
# Результат:
# {
#     "currency_code": "USD",
#     "rate": 72.7384
# }

def get_currency_rate(currency_code):
    url = f"https://www.cbr-xml-daily.ru//daily_json.js"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to get currency rate")
    data = response.json()
    currency_data = data["Value"].get(currency_code)
    if not currency_data:
        raise ValueError(f"No data for currency {currency_code}")
    return {
        "currency_code": currency_code,
        "rate": currency_data["Value"],
    }

# Задача 5
from datetime import datetime, timedelta

def add_week_to_dates(dates: list[str]) -> list[str]:
    output_dates = []
    for date in dates:
        date_obj = datetime.strptime(date, '%Y.%m.%d')
        new_date_obj = date_obj + timedelta(days=7)
        output_dates.append(new_date_obj.strftime('%B %#d, %Y'))
    return output_dates


# Задача 6 (datetime)
import json
from datetime import datetime

def event_durations(json_str):
    events = json.loads(json_str)
    durations = []
    for event in events:
        start_date = datetime.strptime(event['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(event['end_date'], '%Y-%m-%d')
        duration = (end_date - start_date).days
        durations.append(duration)
    return durations

# input data example:
# [
#   {
#     "name": "Event 1",
#     "start_date": "2022-01-01",
#     "end_date": "2022-01-05"
#   },
#   {
#     "name": "Event 2",
#     "start_date": "2022-02-15",
#     "end_date": "2022-02-18"
#   },
#   {
#     "name": "Event 3",
#     "start_date": "2022-03-10",
#     "end_date": "2022-03-20"
#   }
# ]