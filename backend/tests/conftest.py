"""Pytest fixtures: in-memory SQLite + an ASGI client with get_db overridden.

No real Postgres or Supabase needed — tests mint their own HS256 JWTs with
TEST_JWT_SECRET, which is also what the app is configured to verify against.
"""

import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# CRITICAL ordering: set env BEFORE importing the app, because app.core.config
# builds its Settings() singleton at import time — these must already be present.
TEST_JWT_SECRET = "test-jwt-secret-that-is-long-enough-for-hs256"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_JWT_SECRET"] = TEST_JWT_SECRET  # app verifies HS256 tokens against this

# noqa: E402 — these imports are intentionally below the env setup above.
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import app.models  # noqa: E402,F401 — import registers models on Base.metadata
from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def db_session():
    # A brand-new in-memory DB per test = full isolation.
    # StaticPool pins ONE connection so the tables created below are visible to
    # the request handlers (a fresh connection would get an empty :memory: DB).
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},  # allow the conn across async tasks
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # build the schema for this test
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session            # hand the session to the test (and to override_get_db)
    await engine.dispose()       # tear down the in-memory DB after the test


@pytest_asyncio.fixture
async def async_client(db_session):
    # Make every route in the app use the test's session instead of the real DB.
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    # ASGITransport talks to the app in-process (no network, no running server).
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()  # don't leak the override into other tests
