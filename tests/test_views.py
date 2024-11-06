from unittest.mock import patch
from src.views import get_price_stock

#@patch("requests.get")
#def test_currency_rate(mock_get):
 #   """Тестирование функции, передающей курсы валют"""
  #  mock_get.return_value.json.return_value = {"result": 73.15}
   # assert currency_rate("USD") == 73.15


# курс валют на 2021-07-01


from datetime import datetime
from src.views import greet_user
import pytest

from unittest.mock import patch


@patch("src.views.datetime")
@pytest.mark.parametrize(
    "current_hour, expected_greeting",
    [
        (8, "Доброе утро!"),
        (14, "Добрый день!"),
        (21, "Добрый вечер!"),
        (3, "Доброй ночи!"),
    ],
)
def test_greet_user(mock_datetime, current_hour, expected_greeting):
    mock_now = datetime(2021, 7, 25, current_hour, 0, 0)
    mock_datetime.datetime.now.return_value = mock_now
    result = greet_user(current_hour)
    assert result == expected_greeting

def test_get_price_stocks():
    """Тестирование функции, передающей цены на акции"""
    assert get_price_stock("TSLA") == 252.043