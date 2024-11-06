import sys
from pathlib import Path

from src.config import ROOT_PATH

sys.path.append(str(Path(__file__).resolve().parent.parent))
import json
import logging
from pathlib import Path

from src.reports import spending_by_category
from src.services import creat_dict, investment_bank
from src.utils import currency_conversion, data_to_df
from src.views import filter_operations, get_price_stock, greet_user, hour

path_to_file = Path(ROOT_PATH, "../data/operations.xlsx")

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/main.log")
file_formatted = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
file_handler.setFormatter(file_formatted)
logger.addHandler(file_handler)

def main():
    """Функция упраления проектом"""
    global month
    logger.info("Программа запущена")
    name_user = input(f"Введите имя: \n")
    print(f"{name_user}, {greet_user(hour)}")
    print("""Добро пожаловать в раздел "Главная страница"! """)
    print("Предлагаем ознакомиться с курсом валют и акций.")
    currency_conversion("USD")
    currency_conversion("EUR")
    get_price_stock("GOOGL")
    get_price_stock("TSLA")
    get_price_stock("AMZN")
    get_price_stock("AAPL")

    filter_operations()

    # Следующий раздел
    print(
        """Добро пожаловать в раздел 'Сервис'
    Предлагаем ознакомиться с возможностями Инвест-копилки.
    Хотите знать, сколько денег Вы могли бы отложить в Инвест-копилку за месяц?
    """
    )
#while True:
    es_no = input("Введите 'да' или 'нет': ").lower()
    if es_no == "да":
        # Читаем данные из excel-файла
        transactions = creat_dict(path_to_file)
        logger.info("excel-файл прочитан")
        # Запрашиваем лимит округления
        while True:
            limit = int(
                input(
                    "Выберите комфортную Вам сумму округления остатка для инвесткопилки."
                    "Введите число 10, 50 или 100: "
                )
            )
            if limit == 10 or limit == 50 or limit == 100:
                print(f"Выбрано округление до {limit} рублей")
                break
            elif limit != 10 or limit != 50 or limit != 100:
                print("Ошибка ввода")
                continue
        # Запрашиваем месяц
        while True:
            month_choice = int(
                input(
                    f"Для расчета возьмём 2021 год. Введите порядковый номер месяца от 1 до 12: "
                )
            )
            if 0 < month_choice < 10:
                month = "2021-0" + str(month_choice)
                break
            elif 9 < month_choice < 13:
                month = "2021-" + str(month_choice)
                break
            else:
                print("Ошибка. Введите число в диапазоне от 1 до 12.")
                continue
                break
        total_investment = investment_bank(month, transactions, limit)
        logger.info(f"Производим расчет сумм для инвесткопилки")
        # создаем json-строку
        data = {"total_investment": total_investment}
        json_data = json.dumps((data))
        print(f"Json-ответ: {json_data}")
        # return json_data
    elif es_no == "нет":
        print("Хорошо. До встречи!")
        #break
    else:
        logger.error("Ошибка")
        print("Ошибка ввода")
        #continue

    print("Добро пожаловать в раздел Отчёты!")
    transactions = data_to_df(path_to_file)
    spending_by_category(transactions, "Супермаркеты")
    logger.info(f"Работа программы завершена")
    return print("Программа завершает свою работу, до новых встреч!")


if __name__ == "__main__":
    main()
