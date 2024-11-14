import os.path
from unittest.mock import patch

import pytest

from src.utils import currency_conversion, read_xlsx_file


@pytest.fixture()
def path_test():
    return os.path.join(os.path.abspath(__file__), '../../data/OperationsTest.xlsx')


def test_read_xlsx_file(path_test):
    assert read_xlsx_file(path_test) == [
        {
            'Валюта платежа': 'RUB',
            'Дата платежа': '31.12.2021',
            'Категория': 'Супермаркеты',
            'Номер карты': '*7197',
            'Описание': 'Колхоз',
            'Статус': 'OK',
            'Сумма платежа': -160.89,
        },
        {
            'Валюта платежа': 'RUB',
            'Дата платежа': '31.12.2021',
            'Категория': 'Супермаркеты',
            'Номер карты': '*7197',
            'Описание': 'Колхоз',
            'Статус': 'OK',
            'Сумма платежа': -64,
        },
    ]


@patch('requests.get')
def test_currency_conversion_usd(mock_get):
    mock_response = {
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"rate": 75.25},
        "date": "2024-11-05",
        "historical": False,
        "result": 75.25
    }
    mock_get.return_value.json.return_value = mock_response
    rate = currency_conversion("USD")
    assert rate == 75.25


@patch('requests.get')
def test_currency_conversion_eur(mock_get):
    mock_response = {
        "query": {"from": "EUR", "to": "RUB", "amount": 1},
        "info": {"rate": 90.50},
        "date": "2024-11-05",
        "historical": False,
        "result": 90.50
    }
    mock_get.return_value.json.return_value = mock_response
    rate = currency_conversion("EUR")
    assert rate == 90.50
