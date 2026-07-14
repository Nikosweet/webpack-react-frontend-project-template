from __future__ import annotations
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
import asyncio
from typing import AsyncGenerator
from database.database_url import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False, # Вывод SQL-запросов в консоль
    pool_size = 5, # Количество возможных подключений
    max_overflow=10, # Доп. подключения при перегрузе (pool_size + max_overflow)
)

session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

