from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from schemas.settings import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = f'{settings.DB_TYPE}://{settings.DB_USER}:{settings.DB_PASS}'\
                          f'@{settings.DB_HOST}/{settings.DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
