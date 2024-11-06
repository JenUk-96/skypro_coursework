import pytest
from src.services import investment_bank


@pytest.fixture()
def information():
    return [
        {
            "Дата операции": "01.02.2021 20:27:51",
            "Дата платежа": "04.02.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Кешбэк": 0,
            "Категория": "Красота",
            "МСС": 5977,
            "Описание": "OOO Balid",
            "Бонусы (включая кешбэк)": 6,
            "Округление на Инвесткопилку": 0,
            "Сумма операции с округлением": 316,
        },
        {
            "Дата операции": "01.01.2021 12:49:53",
            "Дата платежа": "01.01.2021",
            "Номер карты": 0,
            "Статус": "OK",
            "Сумма операции": -3000,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Кешбэк": 0,
            "Категория": "Переводы",
            "МСС": 0,
            "Описание": "Линзомат ТЦ Юность",
            "Бонусы (включая кешбэк)": 0,
            "Округление на Инвесткопилку": 0,
            "Сумма операции с округлением": 3000,
        },
    ]


@pytest.fixture()
def month():
    return "2021-02"


@pytest.fixture()
def limit():
    return 100


def test_investment_bank(month, information, limit):
    assert investment_bank(month, information, limit) == 84


def test_investment_bank_zero(month, information, limit):
    assert investment_bank(month, [], limit) == 0