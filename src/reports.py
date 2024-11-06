import logging

import pandas as pd

from src.utils import data_to_df, path_to_file

logger = logging.getLogger("report.log")
#file_handler = logging.FileHandler("logs/report.log", "w", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
#file_handler.setFormatter(file_formatter)
#logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def spending_by_category(
        transactions: pd.DataFrame, category: str, date: [str] = None
) -> pd.DataFrame:
    # """Функция-отчет по транзакциям в указанной категории"""
    df = transactions
    date = pd.to_datetime("31.07.2021", format="%d.%m.%Y")  # '2021-07-31'
    # # Указываем дату, от которой нужно отобрать последние три месяца
    if date == None:
        date = pd.to_datetime("31.07.2021", format="%d.%m.%Y")
    # Вычисляем дату начала периода (3 месяца назад)
    start_date = date - pd.Timedelta(days=92)

    # Фильтруем дата фрейм по дате
    filtered_df = df[
        (pd.to_datetime(df["Дата операции"], dayfirst=True) >= start_date)
        & (pd.to_datetime(df["Дата операции"], dayfirst=True) <= date)
        ]

    # рассчитываем сумму расходов по каждой категории
    sum_price_by_category = filtered_df.groupby("Категория")["Сумма операции"].sum()

    # выводим сумму расходов в заданной категории
    result = print(
        f"Траты в категории {category} за последние 3 месяца составили {sum_price_by_category[category]} руб.")
    logger.info("Выдаю данные по расходам в категории")
    return result


if __name__ == "__main__":
    transactions = data_to_df(path_to_file)
    print(transactions.head())

    spending_by_category(transactions, "Супермаркеты")
