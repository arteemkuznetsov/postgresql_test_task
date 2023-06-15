import os
import csv
from models import Csv
from db_handler import Database


def main():
    """Точка входа"""
    print('uploading tables started')
    db = Database()
    csv_paths = search_csv_files()
    upload_csv_files(csv_paths, db)
    update_counts_in_table(db)
    print('uploading tables finished')


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
    db.create_table()
    for path in paths:
        rows = read_csv(path)
        mappings = create_mappings_to_insert(rows)
        db.bulk_insert(mappings)


def create_mappings_to_insert(rows: list) -> list:
    """
    Созданет список строк для вставки в таблицу
    :param rows: построчно прочитанный csv-файл
    :return: список строк для вставки в таблицу
    """
    mappings = []
    for row in rows:
        mappings.append(
            Csv(
                category=row['category'],
                count=row['count']
            )
        )
    return mappings


def update_counts_in_table(db: Database):
    """
    Подсчитывает количество разных значений category в таблице,
    для каждой category обновляет count в соответствие с подсчетами
    :param db: объект класса Database
    """
    counted_categories = db.get_counted_categories()
    for row in counted_categories:
        db.update_categories_count(row[0], row[1])


if __name__ == "__main__":
    main()
