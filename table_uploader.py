import os
import csv
from models.main import Csv, Base
from db_handler import db, Database


def main():
    """Точка входа"""
    csv_paths = search_csv_files()
    upload_csv_files(csv_paths, db)
    update_counts_in_table(db)


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


def read_csv(path: str) -> list | None:
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


def upload_csv_files(paths: str, db: Database):
    """
    Создает в базе данных таблицу, читает все csv-файлы и вставляет их в таблицу
    :param paths: список путей к csv-файлам
    :param db: объект класса Database
    """
    Base.metadata.create_all(db.engine)
    with db.Session() as session:
        for path in paths:
            rows = read_csv(path)
            db.insert_csv(session, rows, Csv)


def update_counts_in_table(db: Database):
    """
    Подсчитывает количество разных значений category в таблице,
    для каждой category обновляет count в соответствие с подсчетами
    :param db: объект класса Database
    """
    with db.Session() as session:
        counted_categories = db.get_counted_categories(session, Csv)
        for row in counted_categories:
            db.update_categories_count(session, Csv, row[0], row[1])


main()
