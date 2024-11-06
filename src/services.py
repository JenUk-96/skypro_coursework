# from src.date import month
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import openpyxl

logger = logging.getLogger('services')
logger.setLevel(logging.INFO)
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")  # поднимаемся на один уровень вверх
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(log_dir, 'services.log'))
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

date_obj = datetime(2021, 5, 31)
str_date_service = datetime.strftime(date_obj, "%Y-%m")


def creat_dict(path_to_file: str) -> list:
    workbook = openpyxl.load_workbook(path_to_file)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    transactions = []
    try:
        logger.info("Создали список словарей")
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))
            transactions.append(
                {
                    "Дата операции": row_data["Дата операции"],
                    "Дата платежа": row_data["Дата платежа"],
                    "Номер карты": row_data["Номер карты"],
                    "Статус": row_data["Статус"],
                    "Сумма операции": row_data["Сумма операции"],
                    "Валюта операции": row_data["Валюта операции"],
                    "Сумма платежа": row_data["Сумма платежа"],
                    "Валюта платежа": row_data["Валюта платежа"],
                    "Кэшбэк": row_data["Кэшбэк"],
                    "Категория": row_data["Категория"],
                    "MCC": row_data["MCC"],
                    "Описание": row_data["Описание"],
                    "Бонусы (включая кэшбэк)": row_data["Бонусы (включая кэшбэк)"],
                    "Округление на инвесткопилку": row_data["Округление на инвесткопилку"],
                    "Сумма операции с округлением": row_data["Сумма операции с округлением"],
                }
            )
            if len(transactions) == 1500:
                return transactions
                break
    except Exception as e:
        logger.error(f"Ошибка с созданием списка словарей: {e}.")
        print(f"Ошибка с созданием списка словарей: {e}.")


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int):
    """Функция, возвращающая сумму, которую можно было бы отложить в Инвесткопилку
    в заданном месяце года при заданном округлении"""
    logger.info('Запуск работы функции расчета выгоды инвесткопилки')
    # month_choice = month(0)

    operations = []
    for transaction in transactions:
        date_excel = transaction["Дата операции"]
        operation_data = datetime.strptime(date_excel, "%d.%m.%Y %H:%M:%S")
        format_date = operation_data.strftime("%Y-%m-%d %H:%M:%S")
        transaction["Дата операции"] = format_date
        if month in transaction["Дата операции"]:
            operations.append(transaction)
    # print(operations)
    total_investment = 0
    for operation in operations:
        amount = operation["Сумма операции"]

        ceshback = abs(amount) * -1 // limit * -1 * limit
        investment = ceshback - abs(amount)
        operation["Кэшбэк"] = investment  # заполняем в словаре значение кешбэка
        # суммируем кэшбэк за указанный месяц
        total_investment += investment
        total_investment = round(total_investment, 2)
    logger.info('Выводим сообщение о накопленных средствах')
    print(
        f"Итого за {month} в инвесткопилку была бы отложена сумма {total_investment} руб."
    )
    return total_investment

# if __name__ == "__main__":
#    print(investment_bank(str_date_service, creat_dict(path_to_file), 100))
