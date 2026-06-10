"""Tests for the demo-data seeder (CC-29)."""

from sqlalchemy import func, select

from app.models.listing import Listing
from app.models.resource import Resource
from app.services.seeding import SAMPLE_LISTINGS, SAMPLE_RESOURCES, seed_demo


async def _count(db, model) -> int:
    return await db.scalar(select(func.count()).select_from(model))


async def test_seed_populates_resources_and_listings(db_session):
    added = await seed_demo(db_session)
    assert added["resources"] == len(SAMPLE_RESOURCES)
    assert added["listings"] == len(SAMPLE_LISTINGS)
    assert await _count(db_session, Resource) == len(SAMPLE_RESOURCES)
    assert await _count(db_session, Listing) == len(SAMPLE_LISTINGS)


async def test_seed_is_idempotent(db_session):
    await seed_demo(db_session)
    added_again = await seed_demo(db_session)
    # Second run adds nothing and does not duplicate.
    assert added_again == {"resources": 0, "listings": 0}
    assert await _count(db_session, Resource) == len(SAMPLE_RESOURCES)
    assert await _count(db_session, Listing) == len(SAMPLE_LISTINGS)


async def test_seeded_data_drives_recommendations(async_client, db_session):
    """End-to-end smoke: after seeding, a resident gets real recommendations."""
    await seed_demo(db_session)

    import time
    import uuid

    import jwt

    from tests.conftest import TEST_JWT_SECRET

    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register", json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@t.com", "role": "client"}
    )
    token = jwt.encode({"sub": uid, "exp": int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    await async_client.post(
        "/intake",
        json={"food_access_need": True, "housing_assistance_type": "section8", "location": "Wilmington, DE"},
        headers=headers,
    )

    r = await async_client.get("/recommendations/me", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert len(body["resources"]) > 0   # food bank etc.
    assert len(body["housing"]) > 0     # Section 8 listings
