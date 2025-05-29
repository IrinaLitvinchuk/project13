import pytest
from json_practice import generate_users, get_currency_rate, event_durations  # Импортируем из файла с функцией
import requests

# тесты к задаче 1
@pytest.fixture
def data():
    return {
        'first_names': ['John', 'Jane', 'Mark', 'Emily', 'Michael', 'Sarah'],
        'last_names': ['Doe', 'Smith', 'Johnson', 'Brown', 'Lee', 'Wilson'],
        'cities': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']
    }

def test_generate_users_num_users(data):
    """Проверяет, что количество сгенерированных пользователей равно запрошенному количеству пользователей."""
    num_users = 5
    users = [next(generate_users(**data)) for _ in range(num_users)]
    assert len(users) == num_users


def test_generate_users_keys(data):
    """Проверяет, что у всех сгенерированных пользователей есть правильные ключи."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert set(user.keys()) == {'first_name', 'last_name', 'age', 'city'}


def test_generate_users_first_names(data):
    """Проверяет, что у всех сгенерированных пользователей имя является одним из возможных имен."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert user['first_name'] in data['first_names']


def test_generate_users_last_names(data):
    """Проверяет, что у всех сгенерированных пользователей фамилия является одной из возможных фамилий."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert user['last_name'] in data['last_names']


def test_generate_users_age(data):
    """Проверяет, что у всех сгенерированных пользователей возраст находится в заданном диапазоне."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert 18 <= user['age'] <= 65


def test_generate_users_cities(data):
    """Проверяет, что у всех сгенерированных пользователей город является одним из возможных городов."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert user['city'] in data['cities']


# тесты к задаче 3
import json
from unittest.mock import patch, Mock

from json_practice import get_user_info, get_user_repos, get_github_users

@patch('src.github.requests.get')
def test_get_user_info(mocked_get):
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {'login': 'test_user', 'public_repos': 10}
    result = get_user_info('test_user')
    assert result == (True, {'login': 'test_user', 'public_repos': 10})

@patch('src.github.requests.get')
def test_get_user_info_invalid(mocked_get):
    mocked_get.return_value.json.return_value = {'message': 'Not Found'}
    result = get_user_info('non_existent_user')
    assert result == (False, {})

@patch('src.github.requests.get')
def test_get_user_repos(mocked_get):
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
    result = get_user_repos('test_user')
    assert result == (True, ['repo1', 'repo2'])

@patch('src.github.requests.get')
def test_get_user_repos_invalid(mocked_get):
    mocked_get.return_value.status_code = 404
    mocked_get.return_value.json.return_value = {'message': 'Not Found'}
    result = get_user_repos('non_existent_user')
    assert result == (False, [])

@patch('src.github.get_user_info')
@patch('src.github.get_user_repos')
def test_get_github_users(mock_get_user_repos, mock_get_user_info):
    mock_get_user_info.return_value = (True, {'login': 'user1', 'public_repos': 2})
    mock_get_user_repos.return_value = (True, ['repo1', 'repo2'])
    expected_result = [{'login': 'user1', 'public_repos': 2, 'repositories': ['repo1', 'repo2']}]
    result = get_github_users(['user1'])
    assert result == json.dumps(expected_result)

@patch('src.github.get_user_info')
@patch('src.github.get_user_repos')
def test_get_github_users_negative(mock_get_user_repos, mock_get_user_info):
    mock_get_user_info.return_value = (False, {})
    mock_get_user_repos.return_value = (False, [])
    result = get_github_users(['non_existent_user'])
    assert result == None


# тесты к задаче 4
def test_get_currency_rate_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Valute": {
            "USD": {
                "Value": 73.5
            }
        }
    }

    with patch('requests.get', return_value=mock_response):
        result = get_currency_rate("USD")
        assert result == {
            "currency_code": "USD",
            "rate": 73.5
        }


def test_get_currency_rate_no_currency():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Valute": {
            "EUR": {
                "Value": 89.5
            }
        }
    }

    with patch('requests.get', return_value=mock_response):
        with pytest.raises(ValueError, match="No data for currency"):
            get_currency_rate("USD")


def test_get_currency_rate_failed_request():
    mock_response = Mock()
    mock_response.status_code = 500

    with patch('requests.get', return_value=mock_response):
        with pytest.raises(ValueError, match="Failed to get currency rate"):
            get_currency_rate("USD")


 # тест к задаче 5 (datetime)
from json_practice import add_week_to_dates


def test_add_week_to_dates():
    assert add_week_to_dates(["2022.12.31", "2023.1.7"]) == ["January 7, 2023", "January 14, 2023"]
    assert add_week_to_dates([]) == []


# тест к задаче 6 (datetime)
def test_event_durations():
    json_str = '[{"name": "Event 1", "start_date": "2022-01-01", "end_date": "2022-01-05"}, {"name": "Event 2", "start_date": "2022-02-15", "end_date": "2022-02-18"}, {"name": "Event 3", "start_date": "2022-03-10", "end_date": "2022-03-20"}]'
    assert event_durations(json_str) == [4, 3, 10]
