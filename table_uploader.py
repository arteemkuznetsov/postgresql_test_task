import os
import csv
import sqlalchemy as sqla
import sqlalchemy.orm
from models import Csv

DATABASE_URI = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'


def main():
    """Точка входа"""
    engine = sqla.create_engine(DATABASE_URI)
    Session = sqla.orm.sessionmaker(bind=engine)

    csv_paths = search_csv_files()
    write_csv_to_table(engine, Session, csv_paths)
    update_counts_in_table(Session)


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


def create_table(engine):
    """Создает таблицу в базе данных, если ее нет"""
    inspect = sqla.inspect(engine)
    if not inspect.has_table('csv', schema="public"):
        Csv.Base.metadata.create_all(engine)


def write_csv_to_table(engine, Session, paths):
    """Создает в базе данных таблицу, поочередно построчно читает csv-файлы и выполняет запись в таблицу"""
    create_table(engine)
    session = Session()
    for path in paths:
        rows = read_csv(path)
        mappings = []
        for row in rows:
            mappings.append(
                Csv.Csv(
                    category=row['category'],
                    count=row['count']
                )
            )
        session.bulk_save_objects(mappings)
    session.close()


def update_counts_in_table(Session):
    """
    Подсчитывает количество разных значений category в таблице,
    для каждой category обновляет count в соответствие с подсчетами
    """
    session = Session()

    counted_categories_tbl = session.query(Csv.Csv.category, sqla.func.count(Csv.Csv.category)).group_by(
        Csv.Csv.category).all()
    for row in counted_categories_tbl:
        session.query(Csv.Csv).filter(Csv.Csv.category == row[0]).update({'count': row[1]})
        session.commit()

    session.close()


main()
