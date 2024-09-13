import asyncio
from typing import Any
from typing import Generator

import asyncpg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.settings import settings
from src.database import get_db, Base
from src.main import app

CLEAN_TABLES = [
    'logs'
    "contacts",
]


# engine = create_async_engine(settings.db_test.url, future=True, echo=True)
# AsyncSessionLocalTest = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# async def get_session() -> AsyncSession:
#     engine = create_async_engine(settings.db_test.url, future=True, echo=True)
#
#     AsyncSessionLocalTest = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#
#     async with AsyncSessionLocalTest() as session:
#         yield session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="session")
# async def asyncpg_pool():
#     pool = await asyncpg.create_pool(
#         "".join(settings.db_test.url.split("+asyncpg"))
#     )
#     yield pool
#     pool.close()


@pytest.fixture(scope='session', autouse=True)
async def setup_test_db():
    engine = create_async_engine(settings.db_test.url, future=True, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.db_test.url_alembic)
    alembic_cfg.set_main_option("script_location", "src/migrations")
    command.upgrade(alembic_cfg, "head")
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    pass


async def get_db_test() -> Generator:
    engine = create_async_engine(settings.db_test.url, future=True, echo=False)
    AsyncSessionLocalTest = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        session_test: AsyncSession = AsyncSessionLocalTest()
        yield session_test
    finally:
        await session_test.close()


# async def get_db_test():
#     try:
#         # create async engine for interaction with database
#         test_engine = create_async_engine(
#             settings.TEST_DATABASE_URL, future=True, echo=True
#         )
#
#         # create session for the interaction with database
#         test_async_session = sessionmaker(
#             test_engine, expire_on_commit=False, class_=AsyncSession
#         )
#         yield test_async_session()
#     finally:
#         pass


# @pytest.fixture(scope="function", autouse=True)
# async def clean_tables():
#     """Old"""
#     engine = create_async_engine(settings.db_test.url, future=True, echo=False)
#     AsyncSessionLocalTest = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#     session_test: AsyncSession = AsyncSessionLocalTest()
#     async with session_test.begin():
#         for table_for_cleaning in CLEAN_TABLES:
#             await session_test.execute(text(f"""TRUNCATE TABLE {table_for_cleaning};"""))


@pytest.fixture(scope="function", autouse=True)
async def clean_tables():
    """New"""
    # Создание асинхронного двигателя для тестовой базы данных
    engine = create_async_engine(settings.db_test.url, future=True, echo=False)
    AsyncSessionLocalTest = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with AsyncSessionLocalTest() as session_test:
        async with session_test.begin():
            # Отключение проверок внешних ключей для SQLite
            # Очистка всех таблиц
            for table in reversed(Base.metadata.sorted_tables):
                await session_test.execute(table.delete())
            # Включение проверок внешних ключей

            await session_test.commit()

@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.db_test.url.split("+asyncpg"))
    )
    yield pool
    pool.close()


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_db] = get_db_test
    with TestClient(app) as client:
        yield client


# @pytest.fixture
# async def create_contact_in_database(asyncpg_pool):
#     async def create_contact_in_database(name: str):
#         async with asyncpg_pool.acquire() as connection:
#             return await connection.execute(
#                 """INSERT INTO contacts (name) VALUES ($1)""", name
#             )
#
#     return create_contact_in_database
