import requests
import json

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

#Получение списка валют
def getCurrencies():
    try:
        list_countries = getCountries().items()
        list_currencies = dict()

        for countryCode, storeCode in list_countries:
            currencies_url = "https://www.asos.com/api/web/countrymetadata/v1/countrySelector/%s?keyStoreDataversion=hnm9sjt-28&lang=ru-RU" % (countryCode)
            response = requests.get(currencies_url).text
            response_json = json.loads(response)
            parsed_response = response_json['data']['currencies']
            list_currency_full = []
            for item_currency in parsed_response:
                list_currency_part = []
                currency = item_currency['currency']
                symbol = item_currency['symbol']
                list_currency_part.append(storeCode)
                list_currency_part.append(currency)
                list_currency_part.append(symbol)
                list_currency_full.append(list_currency_part)
            list_currencies[countryCode] = list_currency_full

    except Exception as ex:
        print("Ошибка при формировании списка стран")
    finally:
        return list_currencies

#Получение списка кодов стран
def getCountries():
    list_countries = dict()
    try:
        countries_url = "https://www.asos.com/api/web/countrymetadata/v1/countrySelector/RU?keyStoreDataversion=hnm9sjt-28&lang=ru-RU"
        response = requests.get(countries_url).text
        response_json = json.loads(response)
        parsed_response = response_json['data']['countries']
        for item in range(len(parsed_response)):
            countryCode = parsed_response[item]['countryCode']
            storeCode = parsed_response[item]['storeCode']
            list_countries[countryCode] = storeCode
    except Exception as ex:
        print("Ошибка при получении списка стран")
    finally:
        return list_countries

#Формирование скриптов
def generate_script():
    list_currencies = getCurrencies().items()
    date_currencies = []
    for countryCode, items in list_currencies:
        for item in items:
            storeCode = item[0]
            currency = item[1]
            symbol = item[2]
            script_list_currencies = "INSERT INTO `currency_market`(`countryCode`, `storeCode`, `currency`, `symbol`) " \
                "VALUES ('%s', '%s', '%s', '%s');"  % (countryCode, storeCode, currency, symbol)
            date_currencies.append(script_list_currencies)
    return date_currencies