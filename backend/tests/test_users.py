"""Tests for the /users endpoints (register, me, update)."""

import time
import uuid

import jwt

from tests.conftest import TEST_JWT_SECRET


def _token(sub: str) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + 3600},
        TEST_JWT_SECRET,
        algorithm="HS256",
    )


def _new_user_body(**overrides) -> dict:
    body = {
        "id": str(uuid.uuid4()),
        "email": f"{uuid.uuid4().hex[:8]}@test.com",
        "full_name": "Test Client",
        "role": "client",
    }
    body.update(overrides)
    return body


async def test_register_creates_user(async_client):
    body = _new_user_body()
    r = await async_client.post("/users/register", json=body)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == body["id"]
    assert data["email"] == body["email"]
    assert data["role"] == "client"


async def test_register_duplicate_id_returns_409(async_client):
    body = _new_user_body()
    assert (await async_client.post("/users/register", json=body)).status_code == 201
    r = await async_client.post("/users/register", json=body)
    assert r.status_code == 409


async def test_register_rejects_bad_role(async_client):
    r = await async_client.post("/users/register", json=_new_user_body(role="hacker"))
    assert r.status_code == 422


async def test_me_returns_registered_user(async_client):
    body = _new_user_body()
    await async_client.post("/users/register", json=body)
    r = await async_client.get(
        "/users/me", headers={"Authorization": f"Bearer {_token(body['id'])}"}
    )
    assert r.status_code == 200
    assert r.json()["email"] == body["email"]


async def test_update_me_changes_full_name(async_client):
    body = _new_user_body(full_name="Old Name")
    await async_client.post("/users/register", json=body)
    headers = {"Authorization": f"Bearer {_token(body['id'])}"}
    r = await async_client.patch("/users/me", json={"full_name": "New Name"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["full_name"] == "New Name"
