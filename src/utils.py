import json
import os.path
import urllib
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

current_date_utils = datetime.now()

load_dotenv()
api_key = os.getenv("API_KEY")

def currency_conversion(currency):
    """функция, которая принимает код валюты и возвращает ее курс на дату 31.07.2021"""
    # currency = "USD"
    amount = 1
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers = {"apikey": api_key})
    result = response.json()
    date = "2024-11-05"
    from_currency = result["query"]["from"]
    to_currency = result["query"]["to"]
    rate = result["info"]["rate"]
    #logging.info("Передаю данные о курсе валют")
    print(f"Дата: {date}; Валюта: {currency}; Курс: {round(rate,2)}")
    return rate


path_to_file = os.path.join(os.path.abspath(__file__), "../../data/operations.xlsx")


def read_xlsx_file(path_to_file):
    pt = pd.read_excel(path_to_file)
    transactions = pt.apply(lambda row: {
            "Дата платежа": row["Дата платежа"],
            "Статус": row["Статус"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
            "Номер карты": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return transactions

def data_to_df(path_to_file):
    df = pd.read_excel(path_to_file)
    #logger.info("Файл формата excel преобразован в DataFrame")
    # print(df.head())
    return df

#if __name__ == "__main__":
#    currency_conversion("EUR")
