"""Tests for the get_current_user dependency (Supabase JWT verification)."""

import time
import uuid

import jwt

from app.models.user import User
from tests.conftest import TEST_JWT_SECRET


def _token(sub: str, exp_offset: int = 3600) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + exp_offset},
        TEST_JWT_SECRET,
        algorithm="HS256",
    )


async def test_missing_token_returns_401(async_client):
    r = await async_client.get("/users/me")
    assert r.status_code == 401


async def test_invalid_token_returns_401(async_client):
    r = await async_client.get(
        "/users/me", headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert r.status_code == 401


async def test_expired_token_returns_401(async_client):
    token = _token(str(uuid.uuid4()), exp_offset=-1)
    r = await async_client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 401


async def test_valid_token_unknown_user_returns_401(async_client):
    token = _token(str(uuid.uuid4()))
    r = await async_client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 401


async def test_valid_token_known_user_returns_200(db_session, async_client):
    user = User(id=uuid.uuid4(), email="client@test.com", role="client")
    db_session.add(user)
    await db_session.commit()

    token = _token(str(user.id))
    r = await async_client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
    assert r.json()["email"] == "client@test.com"
