"""Tests for the /resources endpoints (CC-12 / CC-31)."""

import time
import uuid

import jwt

from tests.conftest import TEST_JWT_SECRET


def _token(sub: str) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm="HS256"
    )


async def _admin_headers(async_client) -> dict:
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register",
        json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@test.com", "role": "admin"},
    )
    return {"Authorization": f"Bearer {_token(uid)}"}


async def _client_headers(async_client) -> dict:
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register",
        json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@test.com", "role": "client"},
    )
    return {"Authorization": f"Bearer {_token(uid)}"}


def _resource(**overrides) -> dict:
    body = {"name": "Food Bank DE", "category": "food", "need_tags": ["food"], "city": "Dover"}
    body.update(overrides)
    return body


# ── Writes are admin-only ─────────────────────────────────────────────────────

async def test_create_requires_auth(async_client):
    assert (await async_client.post("/resources", json=_resource())).status_code == 401


async def test_create_forbidden_for_non_admin(async_client):
    headers = await _client_headers(async_client)
    r = await async_client.post("/resources", json=_resource(), headers=headers)
    assert r.status_code == 403


async def test_admin_can_create(async_client):
    headers = await _admin_headers(async_client)
    r = await async_client.post("/resources", json=_resource(), headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Food Bank DE"
    assert data["need_tags"] == ["food"]
    assert data["is_active"] is True


async def test_create_rejects_bad_category(async_client):
    headers = await _admin_headers(async_client)
    r = await async_client.post("/resources", json=_resource(category="spaceship"), headers=headers)
    assert r.status_code == 422


# ── Reads are public + filterable ─────────────────────────────────────────────

async def test_list_is_public_and_filters_by_category(async_client):
    headers = await _admin_headers(async_client)
    await async_client.post("/resources", json=_resource(name="A", category="food"), headers=headers)
    await async_client.post("/resources", json=_resource(name="B", category="housing"), headers=headers)

    r = await async_client.get("/resources?category=food")  # no auth header
    assert r.status_code == 200
    names = [x["name"] for x in r.json()]
    assert names == ["A"]


async def test_search_by_keyword(async_client):
    headers = await _admin_headers(async_client)
    await async_client.post("/resources", json=_resource(name="Riverside Shelter", category="housing"), headers=headers)
    await async_client.post("/resources", json=_resource(name="Job Center", category="employment"), headers=headers)

    r = await async_client.get("/resources?q=shelter")
    assert [x["name"] for x in r.json()] == ["Riverside Shelter"]


async def test_get_missing_resource_404(async_client):
    r = await async_client.get(f"/resources/{uuid.uuid4()}")
    assert r.status_code == 404


# ── Update + soft-delete ──────────────────────────────────────────────────────

async def test_update_changes_field(async_client):
    headers = await _admin_headers(async_client)
    created = await async_client.post("/resources", json=_resource(), headers=headers)
    rid = created.json()["id"]
    r = await async_client.put(f"/resources/{rid}", json={"city": "Newark"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["city"] == "Newark"


async def test_deactivate_hides_from_default_list(async_client):
    headers = await _admin_headers(async_client)
    created = await async_client.post("/resources", json=_resource(name="OldProgram"), headers=headers)
    rid = created.json()["id"]
    await async_client.post(f"/resources/{rid}/deactivate", headers=headers)

    active = await async_client.get("/resources")
    assert "OldProgram" not in [x["name"] for x in active.json()]
    # still visible when explicitly including inactive
    allres = await async_client.get("/resources?active_only=false")
    assert "OldProgram" in [x["name"] for x in allres.json()]
