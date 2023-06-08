import os
import csv
import psycopg2
import psycopg2.extras
import db_conf


def main():
    """Точка входа"""
    csv_paths = search_csv_files()
    write_csv_to_table(csv_paths)
    update_counts_in_table()


def search_csv_files() -> list:
    """
    Ищет в папке ./out все .csv-файлы
    :return: список путей
    """
    paths = []
    for root, dirs, files in os.walk('./out'):
        for file in files:
            if file.endswith('.csv'):
                paths.append(os.path.join(root, file).replace('\\', '/'))
    return paths


def read_csv(path) -> list | None:
    """
    Читает .csv-файл и приводит все значения поля count к типу int
    :param path: путь к csv-файлу
    :return: список словарей или None
    """
    try:
        with open(path, newline='') as csvfile:
            rows = list(csv.DictReader(csvfile))
            for row in rows:
                row['count'] = int(row['count'])
            return rows
    except IOError:
        return None


def connect() -> psycopg2.connection | None:
    """Подключается к базе данных PostgreSQL"""
    try:
        return psycopg2.connect(
            dbname=db_conf.DATABASE,
            user=db_conf.USERNAME,
            password=db_conf.PASSWORD,
            host=db_conf.HOST
        )
    except psycopg2.OperationalError:
        return None


def select(conn, sql) -> list:
    """Делает SQL-запрос, возвращающий таблицу значений"""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
        curs.execute(sql)
        data = curs.fetchall()
    return data


def query(conn, sql, data=None):
    """Делает SQL-запрос, который ничего не возвращает"""
    with conn.cursor() as curs:
        curs.execute(sql, data)
        conn.commit()


def write_csv_to_table(paths):
    """Создает в базе данных таблицу, поочередно читает csv-файлы, формирует запрос и выполняет запись в таблицу"""
    conn = connect()
    query(conn, 'CREATE TABLE IF NOT EXISTS csv (category VARCHAR(8), count INT)')

    for path in paths:
        rows = read_csv(path)
        data = ()
        sql = 'INSERT INTO csv (category, count) VALUES '
        for index, row in enumerate(rows):
            sql += '(%s, %s),' if index != len(rows) - 1 else '(%s, %s)'
            data = data + (row['category'], row['count'],)
        query(conn, sql, data)

    conn.close()


def update_counts_in_table():
    """
    Подсчитывает количество одинаковых категорий в таблице,
    для каждой category обновляет count в соответствие с подсчетами
    """
    conn = connect()
    categories_count_table = select(conn, 'SELECT category, count(*) AS count FROM csv GROUP BY 1')
    for row in categories_count_table:
        query(conn, 'UPDATE csv SET count = %s WHERE category = %s', (row['count'], row['category']))
    conn.close()


main()
