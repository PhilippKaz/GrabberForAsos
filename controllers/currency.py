import requests

import re
from bs4 import BeautifulSoup

#Получение курса валюты
def Exchange_Currency(currency_from, currency_to):
    try:
        html = requests.get("https://www.calc.ru/kurs-%s-%s.html" % (currency_from, currency_to))
    except Exception as ex:
        print("Возникла ошибка при получении курса валют")
    finally:
        html_soup = BeautifulSoup(html.content, 'html.parser')
        string_rate = str(html_soup.findAll("b")[1])
        rate = re.search("\d*[.]?\d+\d*", string_rate).group(0)
        return rate