import pymysql

from config import host, user, password, db_name
from controllers.asos import *

#Вставка списка валют магазина
def insert_currency_market():
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
                #Добавление списка рынков и валют магазина
                try:
                    scripts = generate_script()
                    for script in scripts:
                        cursor.execute(script)
                except Exception as ex:
                    print("Ошибка при получении данных")
                finally:
                    connection.commit()
        except Exception as ex:
            print('Ошибка подключения')

    finally:
            connection.close()

