from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(AsyncAttrs, DeclarativeBase):
  pass


engine = create_async_engine(str(settings.database_url), echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncIterator[AsyncSession]:
  async with AsyncSessionLocal() as session:
    yield session


async def init_database() -> None:
  # Migrations are handled via Alembic; this function exists for future health checks.
  async with engine.begin() as conn:  # pragma: no cover - simple connectivity check
    await conn.run_sync(lambda _: None)

