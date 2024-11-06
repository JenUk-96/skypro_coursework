from unittest.mock import patch

from src.utils import currency_conversion, read_xlsx_file


@patch("requests.get")
def test_currency_conversion(mock_get):
    """Тестирование функции, передающей курсы валют"""
    mock_get.return_value.json.return_value = {"result": 106.85}
    assert currency_conversion("USD") == 106.85


def path_to_file():
    return "C:\Users\Docto|PycharmProjects\skypro_courcework\data\OperationsTest.xlsx"


def test_read_xlsx_file(path_to_file):
    assert read_xlsx_file(path_to_file) == [
        {
            "Бонусы (включая кешбэк)": 3,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Категория": "Супермаркеты",
            "Кешбэк": 0,
            "МСС": 5411,
            "Номер карты": "*7197",
            "Округление на Инвесткопилку": 0,
            "Описание": "Колхоз",
            "Статус": "OK",
            "Сумма операции": -160.89,
            "Сумма операции с округлением": 160.89,
        },
        {
            "Бонусы (включая кешбэк)": 1,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "31.12.2021 16:42:04",
            "Дата платежа": "31.12.2021",
            "Категория": "Супермаркеты",
            "Кешбэк": 0,
            "МСС": 5411,
            "Номер карты": "*7197",
            "Округление на Инвесткопилку": 0,
            "Описание": "Колхоз",
            "Статус": "OK",
            "Сумма операции": -64,
            "Сумма операции с округлением": 64,
        },
    ]
