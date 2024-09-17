from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.settings import settings

engin = create_async_engine(settings.db_prod.url, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engin, expire_on_commit=False, autocommit=False, autoflush=False, class_=AsyncSession)

Base = declarative_base()

async def get_db() -> Generator:
    try:
        session: AsyncSession = AsyncSessionLocal()
        yield session
    finally:
        await session.close()
