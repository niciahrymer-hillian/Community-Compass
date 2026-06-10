"""Tests for the AI-guided intake assistant (CC-05 / CC-06).

No GROQ key in the test env, so the deterministic rule-based path is exercised.
"""

from app.services.assistant import classify_intent, program_info, suggest_intake


# ── Unit: classification + extraction ─────────────────────────────────────────

def test_classify_picks_dominant_intent():
    out = classify_intent("I was evicted and need an apartment fast")
    assert out["intent"] == "housing"
    assert out["confidence"] > 0


def test_classify_no_keywords_is_general_support():
    out = classify_intent("hello there")
    assert out == {"intent": "general_support", "confidence": 0.0}


def test_suggest_intake_extracts_fields():
    s = suggest_intake("I'm homeless and looking for a section 8 apartment, also need food")
    assert s["housing_status"] == "homeless"
    assert s["housing_assistance_type"] == "section8"
    assert s["food_access_need"] is True


# ── API ───────────────────────────────────────────────────────────────────────

async def test_classify_endpoint(async_client):
    r = await async_client.post("/assistant/classify", json={"message": "I lost my job"})
    assert r.status_code == 200
    assert r.json()["intent"] == "employment"


async def test_chat_returns_reply_and_suggestions(async_client):
    r = await async_client.post(
        "/assistant/chat",
        json={"messages": [{"role": "user", "content": "I need help with groceries and a bus pass"}]},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["reply"]                               # supportive fallback reply
    assert body["suggestions"]["food_access_need"] is True
    assert body["suggestions"]["transportation_need"] is True


async def test_chat_empty_messages_is_general(async_client):
    r = await async_client.post("/assistant/chat", json={"messages": []})
    assert r.status_code == 200
    assert r.json()["intent"] == "general_support"


# ── HomeMatch grounding (HOUSING_CONTEXT) ─────────────────────────────────────

def test_program_info_detects_section8():
    info = program_info("do I qualify for a section 8 voucher?")
    assert len(info) == 1
    assert "Section 8" in info[0]


async def test_chat_grounds_program_questions(async_client):
    r = await async_client.post(
        "/assistant/chat",
        json={"messages": [{"role": "user", "content": "what is SRAP and section 8?"}]},
    )
    assert r.status_code == 200
    body = r.json()
    # HomeMatch's actual program text is surfaced.
    assert len(body["program_info"]) == 2
    assert any("SRAP" in p or "State Rental" in p for p in body["program_info"])
