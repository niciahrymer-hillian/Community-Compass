"""Tests for the dev-login shortcut."""

import app.api.routes.auth as auth_module


async def test_dev_login_issues_working_token(async_client):
    r = await async_client.post("/auth/dev-login", json={"email": "demo@test.com", "role": "client"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    # The minted token works on a protected route.
    me = await async_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "demo@test.com"


async def test_dev_login_is_idempotent_per_email(async_client):
    a = await async_client.post("/auth/dev-login", json={"email": "same@test.com"})
    b = await async_client.post("/auth/dev-login", json={"email": "same@test.com"})
    assert a.json()["user"]["id"] == b.json()["user"]["id"]  # same user, not a duplicate


async def test_dev_login_disabled_returns_404(async_client, monkeypatch):
    monkeypatch.setattr(auth_module.settings, "DEV_LOGIN_ENABLED", False)
    r = await async_client.post("/auth/dev-login", json={"email": "x@test.com"})
    assert r.status_code == 404


async def test_dev_login_works_with_empty_jwt_secret(async_client, monkeypatch):
    # Regression: PyJWT rejects an empty HS256 key; hs256_secret must fall back.
    monkeypatch.setattr(auth_module.settings, "SUPABASE_JWT_SECRET", "")
    assert auth_module.settings.hs256_secret  # non-empty fallback
    r = await async_client.post("/auth/dev-login", json={"email": "empty@test.com"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = await async_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200


async def test_dev_login_switches_role_on_relogin(async_client):
    a = await async_client.post("/auth/dev-login", json={"email": "switch@test.com", "role": "client"})
    assert a.json()["user"]["role"] == "client"
    b = await async_client.post("/auth/dev-login", json={"email": "switch@test.com", "role": "navigator"})
    assert b.json()["user"]["role"] == "navigator"  # same user, role updated
