import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models.settings import settings

DATABASE_URI = \
    f'postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}'


class Database:
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)

    def insert_csv(self, session: sqlalchemy.orm.session.Session, rows: list,
                   Csv: sqlalchemy.orm.decl_api.DeclarativeMeta):
        """
        Множественная вставка строк в таблицу
        :param session: SQLAlchemy sessionmaker
        :param rows: список словарей в формате [{category: str, count: int}, ...]
        :param Csv: модель csv-файла
        """
        mappings = []
        for row in rows:
            mappings.append(
                Csv(
                    category=row['category'],
                    count=row['count']
                )
            )
        session.bulk_save_objects(mappings)

    def update_categories_count(self, session: sqlalchemy.orm.session.Session,
                                Csv: sqlalchemy.orm.decl_api.DeclarativeMeta, category: str, count: int):
        """
        Обновление полей count для каждого поля category
        :param session: SQLALchemy session
        :param Csv: модель csv-файла
        :param category: поле "категория" в таблице
        :param count:  поле "количество" в таблице
        """
        session.query(Csv).filter(Csv.category == category).update({'count': count})
        session.commit()

    def get_counted_categories(self, session: sqlalchemy.orm.session.Session,
                               Csv: sqlalchemy.orm.decl_api.DeclarativeMeta) -> list:
        """
        Подсчет количества каждой категории в таблице
        :param session: SQLAlchemy session
        :param Csv: модель csv-файла
        :return прочитанная таблица
        """
        return session.query(Csv.category, func.count(Csv.category)).group_by(Csv.category).all()


db = Database()
