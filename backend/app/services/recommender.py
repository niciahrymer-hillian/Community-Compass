"""Resource recommendation engine (CC-13), adapting Future-Path's rules.

Future-Path used NEED_PRIORITY + NEED_TAG_MAP to rank a youth's resources by
need. We keep that idea but drive it from Community Compass's intake fields and
match against our Resource.category / need_tags. Every recommendation carries a
reason ("why this was recommended") — an explicit acceptance criterion.
"""

from app.models.intake import Intake
from app.models.resource import Resource

# Need → urgency weight (higher ranks first). Adapted from Future-Path's NEED_PRIORITY.
NEED_PRIORITY = {
    "unstable_housing": 50,
    "safety": 45,
    "food": 40,
    "unemployment": 35,
    "wellness": 30,
    "transportation": 25,
    "documents": 20,
    "education": 15,
    "general_support": 5,
}

# Need → the resource categories/tags that address it (our 12-category vocab).
NEED_CATEGORIES = {
    "unstable_housing": {"housing"},
    "safety": {"safety", "legal_aid"},
    "food": {"food"},
    "unemployment": {"employment", "financial_literacy"},
    "wellness": {"wellness"},
    "transportation": {"transportation"},
    "documents": {"documents"},
    "education": {"education", "mentorship", "youth_services"},
    "general_support": set(),
}

_UNSTABLE_HOUSING = {"unstable", "homeless", "at_risk"}
_UNEMPLOYED = {"unemployed", "none", "not_working"}
_NO_EDUCATION = {"no_diploma", "none"}


def derive_needs(intake: Intake) -> list[str]:
    """Translate intake answers into a list of need keys (most urgent first)."""
    needs: list[str] = []
    if (intake.housing_status or "").lower() in _UNSTABLE_HOUSING:
        needs.append("unstable_housing")
    if intake.safety_concern:
        needs.append("safety")
    if intake.food_access_need:
        needs.append("food")
    if (intake.employment_status or "").lower() in _UNEMPLOYED:
        needs.append("unemployment")
    if intake.health_wellness_need:
        needs.append("wellness")
    if intake.transportation_need:
        needs.append("transportation")
    if (intake.document_status or "").lower() == "missing_id":
        needs.append("documents")
    if (intake.education_status or "").lower() in _NO_EDUCATION:
        needs.append("education")
    # Always have something to say, even with a sparse intake.
    return needs or ["general_support"]


def recommend_resources(
    intake: Intake, resources: list[Resource], top_n: int = 5
) -> list[tuple[Resource, int, list[str]]]:
    """Score resources against the intake's needs; return top_n ranked, with reasons."""
    needs = derive_needs(intake)
    scored: list[tuple[Resource, int, list[str]]] = []

    for resource in resources:
        score = 0
        reasons: list[str] = []
        tags = set(resource.need_tags or [])
        for need in needs:
            cats = NEED_CATEGORIES.get(need, set())
            if resource.category in cats or (tags & cats):
                score += NEED_PRIORITY[need]
                reasons.append(f"Matches your {need.replace('_', ' ')} need")
        # Local resources are easier to reach — small tie-breaker boost.
        if intake.location and resource.city and resource.city.lower() in intake.location.lower():
            score += 5
            reasons.append(f"Located in {resource.city}")
        if score > 0:
            scored.append((resource, score, reasons))

    scored.sort(key=lambda row: row[1], reverse=True)
    return scored[:top_n]
