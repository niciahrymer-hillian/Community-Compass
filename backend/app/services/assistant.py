"""AI-guided intake assistant (CC-05 / CC-06), adapting HomeMatch's ai_service.

The assistant asks supportive questions, classifies what a resident needs (CC-06),
and turns their free-text answers into structured intake fields (CC-05) the
resident can review before saving. It works with **zero API keys** via a
rule-based fallback; when GROQ_API_KEY is set it uses Groq for the conversational
reply. It supports — never replaces — the intake; the human reviews before saving.
"""

import httpx

from app.core.config import settings

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


async def chat(messages: list[dict]) -> dict:
    """Return a reply + the detected intent + suggested intake fields.

    Uses Groq when a real key is configured, otherwise a rule-based reply. Either
    way, intent + suggestions come from the deterministic rules so the structured
    output is stable and testable.
    """
    last_user = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
    intent = classify_intent(last_user)
    suggestions = suggest_intake(last_user)

    if _groq_ready():
        try:
            reply = await _groq_reply(messages, _SYSTEM_PROMPT)
        except Exception:
            reply = _FOLLOW_UP[intent["intent"]]  # never fail the request on AI error
    else:
        reply = _FOLLOW_UP[intent["intent"]]

    return {"reply": reply, **intent, "suggestions": suggestions}
