import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database
from starlette.testclient import TestClient

from database.database import Base, get_db
from main import app
from schemas.settings import Settings


@pytest.fixture(scope="session")
def engine():
    settings = Settings()
    TEST_DB_NAME = f'{settings.DB_NAME}_test'

    SQLALCHEMY_DATABASE_URL = f'{settings.DB_TYPE}://{settings.DB_USER}:{settings.DB_PASS}' \
                              f'@{settings.DB_HOST}/{TEST_DB_NAME}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)

    yield engine

    drop_database(engine.url)


@pytest.fixture(scope="session")
def db(engine):
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides
