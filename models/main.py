from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR

Base = declarative_base()


class Csv(Base):
    __tablename__ = 'csv'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(VARCHAR(8))
    count = Column(Integer)

    def __init__(self, category, count):
        self.category = category
        self.count = count

    def __repr__(self):
        return "<Csv(category='{}', count='{}'".format(self.category, self.count)
