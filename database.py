from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" #строка подключения
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #обязательное условие для корректности работы бд в sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #autoflush=False - мы сами делаем коммиты; autoflush=True - автоматическое создание коммитов

Base = declarative_base()

def get_db(): #функция для открытия подключения к бд и его же закрытия
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()