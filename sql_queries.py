import pymysql
from config import DB_USER, DB_NAME, DB_PASSWORD

# Подключение к БД
def connect_to_DB():
    try:
        connection = pymysql.connect(
            host='localhost',          # Хост базы данных
            user=DB_USER,      # Имя пользователя
            password=DB_PASSWORD,  # Пароль
            database=DB_NAME,  # Название базы данных
            port=3306,                 # Порт (по умолчанию 3306)
            charset='utf8mb4',         # Кодировка
            cursorclass=pymysql.cursors.DictCursor  # Возвращать результаты как словари
        )
        print("Подключение к MySQL успешно установлено")

        return connection
    
    except Exception as ex:
        print(f"Ошибка подключения к MySQL: {ex}")


# Отключение от БД
def disconnect_from_DB(connection: pymysql.cursors.DictCursor, comment: str=None):
    if connection:
        connection.close()
        print(comment)


# Выполнение запросов для БД
def execute_query(connection: pymysql.cursors.DictCursor, query: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print("✅ Запрос выполнен успешно")
        
    except Exception as ex:
        print(f"❌ Ошибка выполнения запроса: {ex}")

        