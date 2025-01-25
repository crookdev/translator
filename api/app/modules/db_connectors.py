import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


class PostgresDB:
    Base = declarative_base()
    
    class Translation(Base):
        __tablename__ = 'translations'
        id = Column(Integer, primary_key=True)
        source_language = Column(String, nullable=False)
        destination_language = Column(String, nullable=False)
        text = Column(String, nullable=False)

    def __init__(self):
        self.DATABASE_URI = f'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/mydatabase'
        self.engine = create_engine(self.DATABASE_URI)
        self.base = declarative_base()
    
    def write_data(self, data):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        row = self.Translation(
            source_language=data[0],
            destination_language=data[1],
            text=data[2]
        )
        session.add(row)

        session.commit()