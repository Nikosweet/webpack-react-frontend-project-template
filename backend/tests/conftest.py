import os
from pathlib import Path
from dotenv import load_dotenv

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from database.database import Base
from database.models.person import PersonOrm
from database.models.product import ProductOrm

env_path = Path(__file__).parent.parent / ".test.env"
load_dotenv(dotenv_path=env_path)


def get_test_database_url():

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "")
    db_name = os.getenv("DB_NAME", "pisdata_test")

    return f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

TEST_DATABASE_URL = get_test_database_url()

@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def test_person_data():
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "phone": '+799999999999',
        'hashpassword': '1234'
    }


@pytest_asyncio.fixture(scope="function")
async def create_test_person(session, test_person_data):
    person = PersonOrm(**test_person_data)
    session.add(person)
    await session.commit()
    await session.refresh(person)
    return person