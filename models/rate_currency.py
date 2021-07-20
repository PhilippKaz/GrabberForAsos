import pymysql
from config import host, user, password, db_name
from controllers.currency import *
import datetime


def rate_currency():
    try:
        connection = pymysql.connect(
            host=host,
            port=3307,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                #Добавление курса валют в таблицу
                try:
                    now = datetime.datetime.now()
                    script_trunc = "TRUNCATE TABLE rate_currency"
                    cursor.execute(script_trunc)
                    script_get_currency_list = "SELECT `currency`FROM `currency_list`"
                    cursor.execute(script_get_currency_list)
                    currency_items = cursor.fetchall()
                    for currency_item in currency_items:
                        currency_from = currency_item['currency']
                        currency_to = "RUB"
                        rate = Exchange_Currency(currency_from, currency_to)
                        script_insert_rate_currency = "INSERT INTO `rate_currency`(`currency_from`, `currency_to`, `rate`, `datetime_update`) VALUES ('%s', '%s', '%s', '%s')" % (currency_from, currency_to, rate, now)
                        try:
                            cursor.execute(script_insert_rate_currency)
                        except Exception as ex:
                            print("Возникла ошибка при вставке курса валют")

                except Exception as ex:
                    print("Ошибка при получении данных")
        finally:
            connection.commit()

    except Exception as ex:
        print('Ошибка подключения')

    finally:
        connection.close()

