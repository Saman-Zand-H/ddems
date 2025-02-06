from collections.abc import AsyncGenerator

from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .constants import MAX_OVERFLOW, POOL_RECYCLE, POOL_SIZE

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_recycle=POOL_RECYCLE,
)
async_session_maker = async_sessionmaker(
    expire_on_commit=False,
    autoflush=False,
    bind=engine,
)


def get_async_session():
    return async_session_maker()


async def get_async_session_generator() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
