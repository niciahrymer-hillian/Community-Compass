"""Tests for /housing listings + eligibility matching (CC-32 / CC-10)."""

import time
import uuid

import jwt

from tests.conftest import TEST_JWT_SECRET


def _token(sub: str) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm="HS256"
    )


async def _user(async_client, role: str) -> tuple[str, dict]:
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register",
        json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@test.com", "role": role},
    )
    return uid, {"Authorization": f"Bearer {_token(uid)}"}


def _listing(**overrides) -> dict:
    body = {"title": "Unit A", "address": "1 Main St", "city": "Dover", "state": "DE", "rent_amount": 1200}
    body.update(overrides)
    return body


# ── CRUD + filters ────────────────────────────────────────────────────────────

async def test_create_listing_is_admin_only(async_client):
    _, client_headers = await _user(async_client, "client")
    assert (await async_client.post("/housing", json=_listing())).status_code == 401
    assert (await async_client.post("/housing", json=_listing(), headers=client_headers)).status_code == 403


async def test_admin_creates_and_public_lists(async_client):
    _, admin = await _user(async_client, "admin")
    r = await async_client.post("/housing", json=_listing(section8_accepted=True, lat=39.1, lng=-75.5), headers=admin)
    assert r.status_code == 201
    assert r.json()["lat"] == 39.1                      # map data present
    listed = await async_client.get("/housing")        # public, no auth
    assert listed.status_code == 200 and len(listed.json()) == 1


async def test_filter_by_program_and_max_rent(async_client):
    _, admin = await _user(async_client, "admin")
    await async_client.post("/housing", json=_listing(title="S8", section8_accepted=True, rent_amount=1000), headers=admin)
    await async_client.post("/housing", json=_listing(title="Market", rent_amount=3000), headers=admin)

    s8 = await async_client.get("/housing?program=section8")
    assert [x["title"] for x in s8.json()] == ["S8"]
    cheap = await async_client.get("/housing?max_rent=1500")
    assert [x["title"] for x in cheap.json()] == ["S8"]


# ── Eligibility matching (CC-10) ──────────────────────────────────────────────

async def test_matches_requires_intake(async_client):
    _, headers = await _user(async_client, "client")
    r = await async_client.get("/housing/matches", headers=headers)
    assert r.status_code == 400  # no intake yet


async def test_matches_rank_eligible_listings_with_reasons(async_client):
    _, admin = await _user(async_client, "admin")
    await async_client.post("/housing", json=_listing(title="S8 Home", city="Dover", section8_accepted=True), headers=admin)
    await async_client.post("/housing", json=_listing(title="Market Home", city="Dover"), headers=admin)

    uid, headers = await _user(async_client, "client")
    await async_client.post(
        "/intake",
        json={"housing_assistance_type": "section8", "location": "Dover, DE"},
        headers=headers,
    )

    r = await async_client.get("/housing/matches", headers=headers)
    assert r.status_code == 200
    matches = r.json()
    # Section 8 listing ranks first and explains why.
    assert matches[0]["listing"]["title"] == "S8 Home"
    assert matches[0]["score"] > matches[1]["score"]
    assert any("Section 8" in reason for reason in matches[0]["reasons"])
    assert any("Dover" in reason for reason in matches[0]["reasons"])
