"""Database session management (async-only)."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings
from app.db.base import Base

engine = create_async_engine(
    str(settings.database_url),
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a request-scoped async SQLAlchemy session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db(create_all: bool = True) -> None:
    """Initialize DB objects for development.

    In production, prefer Alembic migrations over `create_all`.
    """
    if not create_all:
        return
    # Ensure models are imported so mappers are registered
    from app.db import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
