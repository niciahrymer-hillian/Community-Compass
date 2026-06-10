"""Tests for the caseworker/navigator dashboard (CC-23 / CC-24)."""

import time
import uuid

import jwt

from tests.conftest import TEST_JWT_SECRET


def _token(sub: str) -> str:
    return jwt.encode(
        {"sub": sub, "exp": int(time.time()) + 3600}, TEST_JWT_SECRET, algorithm="HS256"
    )


async def _make(async_client, role: str) -> dict:
    uid = str(uuid.uuid4())
    await async_client.post(
        "/users/register", json={"id": uid, "email": f"{uuid.uuid4().hex[:8]}@t.com", "role": role}
    )
    return {"id": uid, "headers": {"Authorization": f"Bearer {_token(uid)}"}}


async def _resident_with_intake(async_client, **intake) -> dict:
    r = await _make(async_client, "client")
    await async_client.post("/intake", json=intake, headers=r["headers"])
    return r


# ── Access control ────────────────────────────────────────────────────────────

async def test_residents_forbidden_for_clients(async_client):
    client = await _make(async_client, "client")
    r = await async_client.get("/caseworker/residents", headers=client["headers"])
    assert r.status_code == 403


async def test_navigator_role_allowed(async_client):
    nav = await _make(async_client, "navigator")  # navigator role now valid (reconciled)
    r = await async_client.get("/caseworker/residents", headers=nav["headers"])
    assert r.status_code == 200


# ── Dashboard data ────────────────────────────────────────────────────────────

async def test_residents_ranked_by_risk_and_filterable(async_client):
    await _resident_with_intake(async_client, housing_status="homeless", safety_concern=True)
    await _resident_with_intake(async_client, housing_status="stable")
    staff = await _make(async_client, "caseworker")

    allr = await async_client.get("/caseworker/residents", headers=staff["headers"])
    body = allr.json()
    assert len(body) == 2
    assert body[0]["risk_score"] >= body[1]["risk_score"]   # most urgent first

    high = await async_client.get("/caseworker/residents?risk=High", headers=staff["headers"])
    assert all(x["risk_level"] == "High" for x in high.json())


async def test_summary_counts(async_client):
    await _resident_with_intake(async_client, housing_status="homeless", document_status="missing_id")
    staff = await _make(async_client, "admin")
    r = await async_client.get("/caseworker/summary", headers=staff["headers"])
    body = r.json()
    assert body["total_residents"] >= 1
    assert body["housing_urgent"] >= 1
    assert body["missing_documents"] >= 1


async def test_resident_profile_has_intake_risk_and_recs(async_client, db_session):
    from app.services.seeding import seed_demo

    await seed_demo(db_session)
    resident = await _resident_with_intake(
        async_client, housing_status="homeless", housing_assistance_type="section8", location="Wilmington, DE"
    )
    staff = await _make(async_client, "caseworker")
    r = await async_client.get(f"/caseworker/residents/{resident['id']}", headers=staff["headers"])
    assert r.status_code == 200
    body = r.json()
    assert body["intake"]["housing_status"] == "homeless"
    assert body["risk"]["level"] in {"Low", "Medium", "High"}
    assert len(body["risk"]["factors"]) > 0
    assert "resources" in body and "housing" in body


async def test_profile_unknown_resident_404(async_client):
    staff = await _make(async_client, "caseworker")
    r = await async_client.get(f"/caseworker/residents/{uuid.uuid4()}", headers=staff["headers"])
    assert r.status_code == 404
