"""Youth risk scoring adapter (CC-04 / Youth Risk section).

Reuses Future-Path's ACTUAL scoring logic — `compute_risk_factors` and
`assign_risk_level` from app/future_path/calculate_risk_scores.py (their verbatim
file) — by translating a Community Compass Intake into the `youth` +
`intake_answers` dicts their functions expect. The scoring rules + weights stay
entirely in the Future-Path teammates' code; this file is only the mapping.
"""

from app.future_path.calculate_risk_scores import assign_risk_level, compute_risk_factors
from app.models.intake import Intake

# our housing_status → Future-Path's housing vocabulary (their factor rules key off these strings)
_HOUSING_MAP = {
    "homeless": "Temporary shelter",
    "unstable": "Couch surfing",
    "at_risk": "At risk of homelessness",
    "stable": "Stable",
}
_UNEMPLOYED = {"unemployed", "none", "not_working"}
_NO_EDUCATION = {"no_diploma", "none", "not_enrolled"}


def _youth_from_intake(intake: Intake) -> dict:
    # compute_risk_factors reads every one of these keys, so provide them all.
    housing = (intake.housing_status or "").lower()
    return {
        "housing": _HOUSING_MAP.get(housing, "Stable"),
        "employment": "Unemployed" if (intake.employment_status or "").lower() in _UNEMPLOYED else "Employed",
        "education": "Not enrolled" if (intake.education_status or "").lower() in _NO_EDUCATION else "Enrolled",
        "mentor_status": "Assigned",     # not captured by our intake yet
        "placement_count": 0,            # not captured by our intake yet
        "prior_homelessness": "Yes" if housing == "homeless" else "No",
    }


def _intake_answers(intake: Intake) -> dict:
    # _truthy() treats "yes" as true; map our boolean need-flags onto their keys.
    return {
        "food_shortage": "yes" if intake.food_access_need else "no",
        "crisis_flag": "yes" if intake.safety_concern else "no",
        "health_need": "yes" if intake.health_wellness_need else "no",
    }


def score_intake(intake: Intake) -> dict:
    """Return an explainable risk result for one intake."""
    factors = compute_risk_factors(_youth_from_intake(intake), _intake_answers(intake))
    total = min(100, sum(f.score for f in factors))   # their weights can exceed 100; cap it
    return {
        "score": total,
        "level": assign_risk_level(total),
        "factors": [{"name": f.name, "score": f.score, "reason": f.reason} for f in factors],
    }
