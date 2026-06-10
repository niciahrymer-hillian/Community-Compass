"""Seed the database with demo data (CC-29).

Run from the backend/ directory:
    .venv/bin/python -m scripts.seed
Uses DATABASE_URL from backend/.env (SQLite by default).
"""

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker

import app.models  # noqa: F401 — register models on Base
from app.core.config import settings
from app.core.database import Base, init_db
from app.services.seeding import seed_demo


async def main() -> None:
    engine = init_db(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        added = await seed_demo(db)
    print(f"Seeded demo data: {added}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
