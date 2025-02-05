from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from .constants import MAX_OVERFLOW, POOL_RECYCLE, POOL_SIZE

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_recycle=POOL_RECYCLE,
    poolclass=QueuePool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
