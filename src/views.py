import datetime
import os

import requests

from src.utils import read_xlsx_file, path_to_file

current_date = datetime.datetime.now()
hour = current_date.hour


def greet_user(hour):
    """Приветствуем пользователя в зависимости от времени суток"""
    if 4 <= hour <= 12:
        return "Доброе утро!"
    elif 12 <= hour <= 18:
        return "Добрый день!"
    elif 18 <= hour <= 22:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def filter_operations():
    """Функция страницы главная: Выводит номера карт, ТОП - 5 трат и КэшБэк"""
    transactions = read_xlsx_file(path_to_file)
    operations = []
    card_numbers = []
    counter_amount = 0
    """Сортировка транзакций за месяц"""
    for transaction in transactions:
        if "07.2021" in str(transaction["Дата платежа"]):
            operations.append(transaction)
            counter_amount += abs(transaction["Сумма платежа"])

            """Записываем номера карт"""
            # logger.info("Начало работы функции ()")
            cards = {}
            result = []
            # logger.info("Перебор транзакций")
            for i in transactions:
                if i["Номер карты"] == "nan" or type(i["Номер карты"]) is float:
                    continue
                elif i["Сумма платежа"] == "nan":
                    continue
                else:
                    if i["Номер карты"][1:] in cards:
                        cards[i["Номер карты"][1:]] += float(str(i["Сумма платежа"])[1:])
                    else:
                        cards[i["Номер карты"][1:]] = float(str(i["Сумма платежа"])[1:])
            for k, v in cards.items():
                result.append({"last_digits": k, "total_spent": round(v, 2), "cashback": round(v / 100, 2)})
            # logger.info("Завершение работы функции (for_each_card)")
            return result
    """Сортировка словаря по величине суммы транзакций в порядке убывания"""
    sorted_operations = sorted(operations, key=lambda x: abs(x["Сумма операции"]), reverse=True)
    """Вывод ТОП-5 транзакций"""
    top_5_transactions = sorted_operations[:5]
    result = []
    count = 0
    for top in top_5_transactions:
        count += 1
        result.append(f"{count}. {top["Категория"]} : {top["Сумма операции"]}")
        # logger.info("Производится расчет топ - 5 транзакций по сумме операций")
        print("Топ - 5 транзакций:")
        for transaction in result:
            print(transaction)
        print("В июле 2021 года операции совершались со следующих банковских карт:")
        for number in card_numbers:
            print(number)
        """Расчет кэшбэка"""
        # logger.info("Рассчитываем кэшбэк")
        cashback = round(counter_amount / 100, 2)
        print(f"Сумма расходов за июль 2021 составляет: {round(counter_amount, 2)} руб.")
        print(f"Сумма кэшбэка за июль 2021 составляет: {cashback}")
        return operations


def get_price_stock(symbol: list) -> list:
    """Функция получения данных об акциях из списка S&P500"""
    # logger.info("Начало работы функции (get_price_stock)")"""Функция, принимающая код акции и возвращающая ее стоимость на дату 01.07.2024"""
    apikey = os.getenv("APIKEY")
    date = "2024-11-01"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={apikey}"
    # Отправка запроса
    response = requests.get(url)
    data = response.json()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=60min&apikey=apikey&month=2024-11&outputsize=1&adjusted=false"
    for day, prices in data["Time Series (Daily)"].items():
        if day == date:
            price = float(prices["1. open"])
            break
    else:
        print(f"Не удалось найти данные для акции на {date}")
    # logger.info("Передаю данные о стоимости акций")
    result = f"Дата: {date}, стоимость акции {symbol} составляет {price}"
    print(result)
    return price


if __name__ == "__main__":
    #get_price_stock("EUR")
    print(get_price_stock("GOOGL"))
    print(get_price_stock("TSLA"))
    # get_price_stock("AMZN")
    # get_price_stock("AAPL")
    # get_price_stock("MSFT")
    print(filter_operations())
