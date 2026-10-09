"""SQLAlchemy connection used by PostgreSQL-backed repositories."""

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    url = get_settings().database_url
    if not url:
        raise RuntimeError("DATABASE_URL es necesaria para usar PostgreSQL")
    return create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=5)
