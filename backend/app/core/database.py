"""Async SQLAlchemy 2.0 engine, session factory, and FastAPI DB dependency.

Adapted from HomeMatch. We standardize on async SQLAlchemy so moving from SQLite
(dev) to Postgres/Supabase (prod) is a URL change, not a rewrite. The portable
ArrayOfString type lets list columns (e.g. housing `programs`) work on both.
"""

from typing import AsyncGenerator

from sqlalchemy import JSON, String, types          # column types + the TypeDecorator base
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY  # native PG array (prod only)
from sqlalchemy.ext.asyncio import (                 # the async variants of engine/session
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase           # 2.0-style declarative base class


class Base(DeclarativeBase):
    """Declarative base all ORM models inherit from."""
    # Every model subclasses this; SQLAlchemy collects their tables on
    # Base.metadata, which create_all / Alembic then build.


class ArrayOfString(types.TypeDecorator):
    """Portable string-array: native ARRAY on PostgreSQL, JSON on SQLite/others."""

    impl = JSON          # the fallback storage type (what SQLite sees)
    cache_ok = True      # tells SQLAlchemy this type is safe to cache in its compiled-query cache

    def load_dialect_impl(self, dialect):
        # Called per-dialect at compile time: choose the real column type.
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_ARRAY(String))  # real array in prod
        return dialect.type_descriptor(JSON())                # JSON blob everywhere else


def _normalize_db_url(url: str) -> str:
    """Ensure the async driver is used for Postgres URLs.

    Render/Supabase hand out `postgres://` or `postgresql://`; SQLAlchemy's async
    engine needs the `+asyncpg` driver. SQLite URLs are left untouched.
    """
    if url.startswith("postgres://"):          # Heroku/Supabase-style scheme
        url = "postgresql+asyncpg://" + url[len("postgres://"):]
    elif url.startswith("postgresql://"):      # standard scheme, but no async driver named
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]
    return url                                  # sqlite+aiosqlite://... falls through unchanged


# Module-level handle to the session factory. None until init_db() runs at startup.
_session_factory: async_sessionmaker[AsyncSession] | None = None


def init_db(database_url: str) -> AsyncEngine:
    """Call once at app startup. Stores the session factory used by get_db."""
    global _session_factory
    engine = create_async_engine(
        _normalize_db_url(database_url),  # make sure the URL has an async driver
        echo=False,                        # set True to log every SQL statement (debugging)
        pool_pre_ping=True,                # check a connection is alive before using it (drops stale conns)
    )
    # expire_on_commit=False → objects stay usable after commit (no surprise reloads).
    _session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine                          # returned so the caller (lifespan) can run create_all / dispose


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields one AsyncSession per request, always closed."""
    assert _session_factory is not None, "Call init_db() before using get_db()"
    # `async with` guarantees the session is closed even if the handler raises.
    async with _session_factory() as session:
        yield session   # FastAPI injects this into the route; code after yield runs on teardown
