"""Tests for youth risk scoring (Future-Path engine adapter)."""

import time
import uuid

import jwt

from app.models.intake import Intake
from app.services.risk import score_intake
from tests.conftest import TEST_JWT_SECRET


# ── Unit: the adapter feeding Future-Path's compute_risk_factors ──────────────

def test_high_risk_intake_scores_high():
    intake = Intake(
        user_id=uuid.uuid4(),
        housing_status="homeless",
        food_access_need=True,
        safety_concern=True,
        health_wellness_need=True,
    )
    result = score_intake(intake)
    names = [f["name"] for f in result["factors"]]
    assert "unstable_housing" in names
    assert "homelessness_risk" in names
    assert "food_shortage" in names
    assert result["level"] in {"Medium", "High"}
    assert result["score"] > 0


def test_stable_intake_scores_low():
    intake = Intake(user_id=uuid.uuid4(), housing_status="stable")
    result = score_intake(intake)
    assert result["score"] == 0
    assert result["level"] == "Low"
    assert result["factors"] == []


# ── API ───────────────────────────────────────────────────────────────────────

async def _user(async_client) -> dict:
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register", json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@t.com", "role": "client"}
    )
    return {"Authorization": f"Bearer {jwt.encode({'sub': uid, 'exp': int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm='HS256')}"}


async def test_risk_requires_intake(async_client):
    headers = await _user(async_client)
    r = await async_client.get("/risk/me", headers=headers)
    assert r.status_code == 400


async def test_risk_returns_explainable_score(async_client):
    headers = await _user(async_client)
    await async_client.post(
        "/intake",
        json={"housing_status": "homeless", "food_access_need": True, "education_status": "no_diploma"},
        headers=headers,
    )
    r = await async_client.get("/risk/me", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["level"] in {"Low", "Medium", "High"}
    assert len(body["factors"]) > 0
    assert all({"name", "score", "reason"} <= set(f) for f in body["factors"])
