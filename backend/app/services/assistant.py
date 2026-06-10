"""AI-guided intake assistant (CC-05 / CC-06), adapting HomeMatch's ai_service.

The assistant asks supportive questions, classifies what a resident needs (CC-06),
and turns their free-text answers into structured intake fields (CC-05) the
resident can review before saving. It works with **zero API keys** via a
rule-based fallback; when GROQ_API_KEY is set it uses Groq for the conversational
reply. It supports — never replaces — the intake; the human reviews before saving.
"""

import httpx

from app.core.config import settings
# HOUSING_CONTEXT is HomeMatch's actual program knowledge (their verbatim
# context_service), so the assistant can explain Section 8 / SRAP / 55+ / LIHTC /
# Fair Housing / income rules accurately — and ground the LLM with the same text.
from app.homematch.context_service import HOUSING_CONTEXT

# Intent → trigger keywords. Order matters only for readability; scoring is by count.
INTENT_KEYWORDS = {
    "housing": ["housing", "evicted", "eviction", "homeless", "shelter", "rent", "apartment", "section 8", "voucher"],
    "food": ["food", "hungry", "groceries", "meal", "snap", "pantry"],
    "employment": ["job", "work", "unemployed", "hired", "income", "career", "training"],
    "transportation": ["ride", "bus", "transport", "car", "commute", "dart"],
    "wellness": ["health", "doctor", "mental", "counseling", "sick", "medical", "therapy"],
    "safety": ["unsafe", "abuse", "danger", "violence", "threat", "scared"],
    "documents": ["id", "identification", "birth certificate", "documents", "papers", "license"],
    "education": ["school", "ged", "diploma", "education", "classes", "college"],
}


def classify_intent(message: str) -> dict:
    """Best-guess need category for a message (CC-06), with a confidence score.

    Confidence is the share of total keyword hits that fell in the winning
    intent. No hits → low-confidence 'general_support' so the caller can show a
    helpful fallback instead of guessing.
    """
    text = (message or "").lower()
    hits = {
        intent: sum(1 for kw in kws if kw in text)
        for intent, kws in INTENT_KEYWORDS.items()
    }
    total = sum(hits.values())
    if total == 0:
        return {"intent": "general_support", "confidence": 0.0}
    best = max(hits, key=hits.get)
    return {"intent": best, "confidence": round(hits[best] / total, 2)}


def suggest_intake(message: str) -> dict:
    """Map free text to structured intake fields (CC-05) for the resident to review."""
    text = (message or "").lower()
    s: dict = {}

    if any(w in text for w in ["homeless", "shelter", "on the street", "nowhere to"]):
        s["housing_status"] = "homeless"
    elif any(w in text for w in ["evicted", "eviction", "lose my home", "behind on rent"]):
        s["housing_status"] = "unstable"

    if "section 8" in text or "voucher" in text:
        s["housing_assistance_type"] = "section8"
    elif "srap" in text:
        s["housing_assistance_type"] = "srap"
    elif any(w in text for w in ["senior", "55+", "55 plus"]):
        s["housing_assistance_type"] = "senior_55plus"

    if any(w in text for w in ["food", "hungry", "groceries", "meal"]):
        s["food_access_need"] = True
    if any(w in text for w in ["ride", "bus", "transport", "car", "commute"]):
        s["transportation_need"] = True
    if any(w in text for w in ["health", "doctor", "mental", "counseling", "sick", "medical"]):
        s["health_wellness_need"] = True
    if any(w in text for w in ["unsafe", "abuse", "danger", "violence", "threat", "scared"]):
        s["safety_concern"] = True
    if any(w in text for w in ["unemployed", "lost my job", "no job", "out of work"]):
        s["employment_status"] = "unemployed"
    if any(w in text for w in ["no id", "lost my id", "birth certificate", "no documents"]):
        s["document_status"] = "missing_id"
    return s


# Supportive next question per intent (used by the rule-based fallback).
_FOLLOW_UP = {
    "housing": "It sounds like housing is a priority. Do you have somewhere safe to stay tonight?",
    "food": "I can help with food access. Are you looking for groceries this week or ongoing food support?",
    "employment": "Let's work on income. Are you currently working at all, even part-time?",
    "transportation": "Getting around matters. Do you need help with bus fare or another way to travel?",
    "wellness": "Your health is important. Are you able to see a doctor or counselor when you need to?",
    "safety": "Your safety comes first. Are you safe right now?",
    "documents": "Missing documents can block other help. Do you have a state ID?",
    "education": "Education opens doors. Are you working toward a diploma, GED, or training?",
    "general_support": "Tell me a bit about what's going on, and I'll point you to the right support.",
}


def _groq_ready() -> bool:
    key = settings.GROQ_API_KEY or ""
    return bool(key) and "placeholder" not in key and len(key) > 20


async def _groq_reply(messages: list[dict], system: str) -> str:
    """Call Groq's OpenAI-compatible chat endpoint for a conversational reply."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.GROQ_BASE_URL.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            json={"model": settings.GROQ_MODEL,
                  "messages": [{"role": "system", "content": system}] + messages},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


_SYSTEM_PROMPT = (
    "You are Community Compass, a warm, practical guide helping a resident find "
    "housing and support. Ask one simple, supportive question at a time. Never give "
    "legal advice. You support intake; the person reviews answers before saving."
)

# Message keywords → HomeMatch HOUSING_CONTEXT program key.
_PROGRAM_KEYWORDS = {
    "section8": ["section 8", "section8", "voucher", "hcv"],
    "srap": ["srap", "state rental"],
    "hopa": ["55+", "55 plus", "senior housing", "older persons", "hopa"],
    "lihtc": ["lihtc", "income-restricted", "income restricted", "tax credit"],
    "fair_housing": ["fair housing", "discriminat", "my rights", "refuse to rent"],
    "income_verification": ["proof of income", "income requirement", "verify income", "ssi", "ssdi"],
}


def program_info(message: str) -> list[str]:
    """Relevant HomeMatch program explanations for a message (grounding)."""
    text = (message or "").lower()
    keys = [k for k, kws in _PROGRAM_KEYWORDS.items() if any(w in text for w in kws)]
    return [HOUSING_CONTEXT[k] for k in keys if k in HOUSING_CONTEXT]


# Detected intent → resource categories to search (the assistant as a search box).
_INTENT_CATEGORIES = {
    "housing": ["housing"],
    "food": ["food"],
    "employment": ["employment", "financial_literacy"],
    "transportation": ["transportation"],
    "wellness": ["wellness"],
    "safety": ["safety", "legal_aid"],
    "documents": ["documents"],
    "education": ["education", "youth_services", "mentorship"],
}

# Intent → the form to launch next (kind, label, intake prefill).
_INTENT_ACTION = {
    "transportation": ("intake", "Request transportation help", {"transportation_need": True}),
    "food": ("intake", "Get food assistance", {"food_access_need": True}),
    "wellness": ("intake", "Get health & wellness support", {"health_wellness_need": True}),
    "safety": ("intake", "Get safety support", {"safety_concern": True}),
    "documents": ("intake", "Get help with documents", {"document_status": "missing_id"}),
    "housing": ("housing", "Browse housing matches", {}),
    "employment": ("intake", "Get employment support", {}),
    "education": ("intake", "Get education support", {}),
}

_YOUTH_KEYWORDS = ["youth", "aging out", "age out", "foster", "young adult", "transition"]


async def match_resources(db, intent: str, limit: int = 3) -> list[dict]:
    """Real resources for the detected need — the assistant's 'search results'."""
    from sqlalchemy import select

    from app.models.resource import Resource

    cats = _INTENT_CATEGORIES.get(intent, [])
    if not cats:
        return []
    rows = (
        await db.scalars(
            select(Resource)
            .where(Resource.is_active.is_(True), Resource.category.in_(cats))
            .limit(limit)
        )
    ).all()
    return [
        {"id": str(r.id), "name": r.name, "category": r.category,
         "contact_phone": r.contact_phone, "website": r.website, "city": r.city}
        for r in rows
    ]


def suggest_action(intent: str, message: str) -> dict | None:
    """Pick the form to offer next: youth → risk, else intent → intake/housing."""
    if any(w in (message or "").lower() for w in _YOUTH_KEYWORDS):
        return {"kind": "risk", "label": "Check your youth risk score", "prefill": {}}
    if intent in _INTENT_ACTION:
        kind, label, prefill = _INTENT_ACTION[intent]
        return {"kind": kind, "label": label, "prefill": prefill}
    return None


async def chat(messages: list[dict]) -> dict:
    """Return a reply + detected intent + intake suggestions + program info.

    Uses Groq when a real key is configured, otherwise a rule-based reply. Either
    way, intent/suggestions/program_info come from deterministic rules so the
    structured output is stable and testable.
    """
    last_user = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
    intent = classify_intent(last_user)
    suggestions = suggest_intake(last_user)
    programs = program_info(last_user)

    if _groq_ready():
        # Ground the LLM with HomeMatch's program knowledge for this message.
        system = _SYSTEM_PROMPT
        if programs:
            system += "\n\nHousing program reference (use this, don't invent):\n" + "\n".join(programs)
        try:
            reply = await _groq_reply(messages, system)
        except Exception:
            reply = _FOLLOW_UP[intent["intent"]]  # never fail the request on AI error
    else:
        reply = _FOLLOW_UP[intent["intent"]]
        # Without an LLM, surface the program explanation directly.
        if programs:
            reply += " " + programs[0]

    return {"reply": reply, **intent, "suggestions": suggestions, "program_info": programs}
