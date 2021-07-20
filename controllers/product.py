import requests
import json

import re

from models.product import *

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

#Получение кода продукта
def getId(url):
    try:
        reg_str = re.search('prd/\d*[?]', url).group(0)
        rep_str_prd = reg_str.replace("prd/", "")
        id_product = rep_str_prd.replace("?", "")
    except:
        id_product = 0
        return id_product
    finally:
        return id_product

#Получение старой цены продукта
def getPrice(json_string):
    parsed_string = json.loads(json_string)
    price = parsed_string['price']['current']['value']
    return price

#Получение минимальной цены
def getMinPrice(url):
    id_product = getId(url)
    if id_product != 0:
        product = Product()
        list_currencies = product.getUniqueCurrency()
        min_price = 1000000000
        global min_price_storeCode
        global min_currency_from
        for currency_item in list_currencies:
            storeCode = currency_item['storeCode']
            currency_from = currency_item['currency']
            url_product = "https://api.asos.com/product/catalogue/v3/products/%s?store=%s&currency=%s" % (id_product, storeCode, currency_from)
            response = requests.get(url_product, headers=headers)
            if response.status_code == 200:
                price = getPrice(response.text)
                rate = product.getRateCurrency(currency_from)
                price_rub = float('{:.2f}'.format(price * rate))
                if min_price > price_rub:
                    min_price = float('{:.2f}'.format(price_rub))
                    min_price_storeCode = storeCode
                    min_currency_from = currency_from
            else:
                continue
        return min_price, min_price_storeCode, min_currency_from, id_product
    else:
        return 0, 0, 0, 0

#Получение информации продукта
def getInfo(product_url):
    product_id = getId(product_url)
    if product_id != 0:
        url = "https://api.asos.com/product/catalogue/v3/products/%s?store=RU&currency=RUB" % product_id
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response = response.text
            json_string = json.loads(response)
            product_name = json_string['name']
            product_price = json_string['price']['current']['text']
            price = json_string['price']['current']['value']
            return product_name, product_price, price
    else:
        return 0, 0, 0








