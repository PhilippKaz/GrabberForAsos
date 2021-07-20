import pymysql

from config import host, user, password, db_name

class Product():
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=3307,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor)
        except Exception as ex:
            print("Ошибка подключения к базе данных")

    try:
        #Получить список уникальных валют
        def getUniqueCurrency(self):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT `storeCode`, `currency` FROM `unique_currency_market`")
                    list_currencies = cursor.fetchall()
                    return list_currencies
            except Exception as ex:
                print("Ошибка в запросе")

        #Получить курс валюты
        def getRateCurrency(self, currency_from):
            try:
                with self.connection.cursor() as cursor:
                    script_getRate = "SELECT `rate` FROM `rate_currency` WHERE `currency_from` LIKE '%s'" % currency_from
                    cursor.execute(script_getRate)
                    rate = cursor.fetchall()[0]['rate']
                    return rate
            except Exception as ex:
                print("Ошибка в запросе")
    finally:
        pass

