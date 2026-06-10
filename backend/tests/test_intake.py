"""Tests for the /intake endpoints (CC-30)."""

import time
import uuid

import jwt

from tests.conftest import TEST_JWT_SECRET


def _token(sub: str) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm="HS256"
    )


async def _make_user(async_client) -> tuple[str, dict]:
    """Register a resident and return (user_id, auth headers)."""
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register",
        json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@test.com", "role": "client"},
    )
    return uid, {"Authorization": f"Bearer {_token(uid)}"}


async def test_create_intake_requires_auth(async_client):
    r = await async_client.post("/intake", json={"age": 30})
    assert r.status_code == 401


async def test_create_intake_succeeds(async_client):
    _, headers = await _make_user(async_client)
    payload = {
        "age": 24,
        "location": "Wilmington, DE",
        "household_size": 3,
        "housing_status": "at_risk",
        "transportation_need": True,
        "housing_assistance_type": "section8",
    }
    r = await async_client.post("/intake", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["age"] == 24
    assert data["transportation_need"] is True
    assert data["status"] == "submitted"
    assert "id" in data and "user_id" in data


async def test_create_intake_rejects_bad_enum(async_client):
    _, headers = await _make_user(async_client)
    r = await async_client.post(
        "/intake", json={"housing_status": "on_the_moon"}, headers=headers
    )
    assert r.status_code == 422


async def test_create_intake_rejects_out_of_range_age(async_client):
    _, headers = await _make_user(async_client)
    r = await async_client.post("/intake", json={"age": 999}, headers=headers)
    assert r.status_code == 422


async def test_list_my_intakes_returns_only_own(async_client):
    _, headers_a = await _make_user(async_client)
    _, headers_b = await _make_user(async_client)
    await async_client.post("/intake", json={"age": 40}, headers=headers_a)
    await async_client.post("/intake", json={"age": 50}, headers=headers_b)

    r = await async_client.get("/intake/me", headers=headers_a)
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["age"] == 40


async def test_get_other_users_intake_is_404(async_client):
    _, headers_a = await _make_user(async_client)
    _, headers_b = await _make_user(async_client)
    created = await async_client.post("/intake", json={"age": 40}, headers=headers_a)
    intake_id = created.json()["id"]

    r = await async_client.get(f"/intake/{intake_id}", headers=headers_b)
    assert r.status_code == 404
