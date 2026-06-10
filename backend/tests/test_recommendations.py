"""Tests for /recommendations/me (CC-13 / CC-33) and the recommender rules."""

import time
import uuid

import jwt

from app.models.intake import Intake
from app.models.resource import Resource
from app.services.recommender import derive_needs, recommend_resources
from tests.conftest import TEST_JWT_SECRET


def _token(sub: str) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm="HS256"
    )


async def _user(async_client, role: str = "client") -> tuple[str, dict]:
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register",
        json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@test.com", "role": role},
    )
    return uid, {"Authorization": f"Bearer {_token(uid)}"}


# ── Unit: the rules engine ────────────────────────────────────────────────────

def test_derive_needs_from_flags():
    intake = Intake(user_id=uuid.uuid4(), food_access_need=True, housing_status="homeless")
    needs = derive_needs(intake)
    assert "unstable_housing" in needs and "food" in needs


def test_derive_needs_defaults_to_general_support():
    assert derive_needs(Intake(user_id=uuid.uuid4())) == ["general_support"]


def test_recommend_ranks_by_need_priority():
    intake = Intake(user_id=uuid.uuid4(), housing_status="homeless", transportation_need=True)
    housing = Resource(name="Shelter", category="housing", need_tags=["housing"])
    transit = Resource(name="Bus Pass", category="transportation", need_tags=["transportation"])
    ranked = recommend_resources(intake, [transit, housing])
    # unstable_housing (50) outranks transportation (25).
    assert ranked[0][0].name == "Shelter"
    assert any("housing" in r for r in ranked[0][2])


# ── API ───────────────────────────────────────────────────────────────────────

async def test_recommendations_requires_intake(async_client):
    _, headers = await _user(async_client)
    r = await async_client.get("/recommendations/me", headers=headers)
    assert r.status_code == 400


async def test_recommendations_returns_resources_and_housing(async_client):
    _, admin = await _user(async_client, "admin")
    await async_client.post(
        "/resources",
        json={"name": "Dover Food Bank", "category": "food", "need_tags": ["food"], "city": "Dover"},
        headers=admin,
    )
    await async_client.post(
        "/housing",
        json={"title": "S8 Unit", "address": "1 St", "city": "Dover", "state": "DE",
              "rent_amount": 900, "section8_accepted": True},
        headers=admin,
    )

    _, headers = await _user(async_client)
    await async_client.post(
        "/intake",
        json={"food_access_need": True, "housing_assistance_type": "section8", "location": "Dover, DE"},
        headers=headers,
    )

    r = await async_client.get("/recommendations/me", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["resources"][0]["resource"]["name"] == "Dover Food Bank"
    assert any("food" in reason for reason in body["resources"][0]["reasons"])
    assert body["housing"][0]["listing"]["title"] == "S8 Unit"
    assert any("Section 8" in reason for reason in body["housing"][0]["reasons"])
