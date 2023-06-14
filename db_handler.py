from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models.main import Csv, Base
from settings import settings

DATABASE_URI = \
    f'postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}'


class Database:
    def __init__(self):
        """Инициализация полей engine, Session"""
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def create_table(self):
        """Создание таблицы для записи Csv-файлов"""
        Base.metadata.create_all(self.engine)

    def bulk_insert(self, mappings: list):
        """
        Множественная вставка строк в таблицу
        :param mappings: список строк для вставки
        """
        with self.Session() as session:
            session.bulk_save_objects(mappings)

    def update_categories_count(self, category: str, count: int):
        """
        Обновление полей count для каждого поля category
        :param category: поле "категория" в таблице
        :param count:  поле "количество" в таблице
        """
        with self.Session() as session:
            session.query(Csv).filter(Csv.category == category).update({'count': count})
            session.commit()

    def get_counted_categories(self) -> list:
        """
        Подсчет количества каждой категории в таблице
        :return прочитанная таблица
        """
        with self.Session() as session:
            return session.query(Csv.category, func.count(Csv.category)).group_by(Csv.category).all()
