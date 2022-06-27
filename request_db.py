import psycopg2
from config_db import *

list = []

try:
    connection = psycopg2.connect(
        host = HOST,
        user = USER,
        password = PASSWORD,
        database = DB_NAME,
        port = PORT
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT *;"
        )

        print(cursor.fetchone())
        list.append(cursor.fetchone())

except Exception as ex:
    print("[ERROR] Ошибка подключения к базе данных", ex)
finally:
    if connection:
        connection.close()
        print("[INFO] Соединение закрыто")
