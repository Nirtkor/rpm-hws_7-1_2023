"""Модуль содержит методы для работы с pSQL."""

from os import getenv
from dotenv import load_dotenv
from psycopg2 import errors, connect

load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


def register_user(username, password):
    """Метод для работы с БД.

    Метод создает таблицу в pSQL,
    передает туда username+password.

    Args:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    """
    conn = connect(
        database=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users ('
        '    id SERIAL PRIMARY KEY,'
        '    username VARCHAR(255) NOT NULL,'
        '    password VARCHAR(255) NOT NULL'
        ');'
    )

    cur.execute(
        'INSERT INTO users (username, password) VALUES (%s, %s);',
        (username, password)
    )

    conn.commit()

    cur.close()
    conn.close()


def check_credentials(username, password):
    """Метод для работы с БД.

    Метод проверяет данные авторизации в pSQL.

    Args:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    """
    conn = connect(
        database=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s;",
        (username, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user is not None


def create_history_table():
    """Метод для работы с БД.

    Метод создает таблицу в pSQL,
    хранит историю запросов.

    """
    try:
        conn = connect(
            database=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        )
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                sol INT NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW()
            );
        ''')
        conn.commit()
    except errors.Error as e:
        print(f"Unable to create table: {e}")
    finally:
        if conn:
            conn.close()


def save_sol(user_id, sol):
    """Метод для работы с БД.

    Метод добавляет в таблицу history
    данные sol.

    Args:
        user_id (str): Имя пользователя.
        sol (int): Номер сола.

    """
    try:
        conn = connect(
            database=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        )
        cur = conn.cursor()

        cur.execute(
            'INSERT INTO user_history (user_id, sol) VALUES (%s, %s);',
            (user_id, sol,)
        )
        conn.commit()
    except errors.Error as e:
        print(f"Unable to save sol: {e}")
    finally:
        if conn:
            conn.close()


def get_user_history(username):
    """Метод для работы с БД.

    Метод выводит таблицу history из pSQL.

    Args:
        username (str): Имя пользователя.

    """
    with connect(
            database=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT sol, timestamp FROM user_history WHERE user_id = %s", (username,))
            return [{'sol': row[0], 'timestamp': row[1].strftime("%Y-%m-%d %H:%M:%S")} for row in cur.fetchall()]


def delete_user(username):
    """Метод для работы с БД.

    Метод удаляет пользователя из pSQL.

    Args:
        username (str): Имя пользователя.

    """
    conn = connect(
        database=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM users WHERE username = %s;
    """, (username,))
    
    cur.execute("""
    DELETE FROM user_history WHERE user_id = %s;
    """, (username,))

    conn.commit()

    cur.close()
    conn.close()
