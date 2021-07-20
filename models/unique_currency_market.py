import pymysql

from config import host, user, password, db_name

#Добавление уникальных валют
def insert_unique_currency_market():
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
                try:
                    script = "SELECT DISTINCT `storeCode`, `currency`, `symbol` FROM `currency_market`"
                    cursor.execute(script)
                    list_unique_currency_market = cursor.fetchall()
                    for unique_currency in list_unique_currency_market:
                        storeCode = unique_currency['storeCode']
                        currency = unique_currency['currency']
                        symbol = unique_currency['symbol']
                        scripts = "INSERT INTO `unique_currency_market`(`storeCode`, `currency`, `symbol`) VALUES ('%s', '%s', '%s')" % (storeCode, currency, symbol)
                        cursor.execute(scripts)
                except Exception as ex:
                    print("Ошибка при получении данных")
        finally:
            connection.commit()

    except Exception as ex:
        print('Ошибка подключения')

    finally:
        connection.close()

