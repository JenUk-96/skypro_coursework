from datetime import datetime
from unittest.mock import patch

import pytest

from src.views import get_price_stock, greet_user


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
