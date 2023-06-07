import os
import csv
import psycopg2
import psycopg2.extras
import db_conf


def main():
    csv_paths = search_csv_files()
    write_csv_to_table(csv_paths)
    update_counts_in_table()


def search_csv_files():
    paths = []
    for root, dirs, files in os.walk('./out'):
        for file in files:
            if file.endswith('.csv'):
                paths.append(os.path.join(root, file).replace('\\', '/'))
    return paths


def read_csv(path):
    try:
        with open(path, newline='') as csvfile:
            rows = list(csv.DictReader(csvfile))
            for row in rows:
                row['count'] = int(row['count'])
            return rows
    except IOError:
        return None


def connect():
    try:
        return psycopg2.connect(dbname=db_conf.DATABASE,
                                user=db_conf.USERNAME,
                                password=db_conf.PASSWORD,
                                host=db_conf.HOST)
    except psycopg2.OperationalError:
        return None


def select(conn, sql):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
        curs.execute(sql)
        data = curs.fetchall()
    return data


def query(conn, sql, data=None):
    with conn.cursor() as curs:
        curs.execute(sql, data)
        conn.commit()


def write_csv_to_table(paths):
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
    conn = connect()
    categories_count_table = select(conn, 'SELECT category, count(*) AS count FROM csv GROUP BY 1')
    for row in categories_count_table:
        query(conn, 'UPDATE csv SET count = %s WHERE category = %s', (row['count'], row['category']))
    conn.close()
