import pymysql

from config import host, user, password, db_name

#Вставка списка валют
def insert_list_currency():
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
                #Добавление валюты в таблицу
                try:
                    script = "SELECT DISTINCT `currency`,`symbol` FROM unique_currency_market"
                    cursor.execute(script)
                    list_currency = cursor.fetchall()
                    for currency_item in list_currency:
                        currency = currency_item['currency']
                        symbol = currency_item['symbol']
                        script_insert_currency_list = "INSERT INTO `currency_list` (`currency`, `symbol`) VALUES ('%s', '%s')" % (currency, symbol)
                        cursor.execute(script_insert_currency_list)
                except Exception as ex:
                    print("Ошибка при получении данных")
        finally:
            connection.commit()

    except Exception as ex:
        print('Ошибка подключения')

    finally:
        connection.close()
