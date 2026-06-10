"""Eligibility matching engine (CC-10), adapted from HomeMatch.

Turns a resident's intake into the housing programs they qualify for, then scores
each listing — with a human-readable reason for every match, so the UI can show
"why this matched" (a core acceptance criterion).
"""

from app.models.intake import Intake
from app.models.listing import Listing

# Internal program key → (human label, the Listing boolean that flags it).
_PROGRAMS = {
    "section8": ("Section 8 voucher", "section8_accepted"),
    "srap": ("SRAP", "srap_accepted"),
    "age55plus": ("55+ housing", "age_55_plus"),
    "income_restricted": ("income-restricted housing", "income_restricted"),
}

# intake.housing_assistance_type value → internal program key.
_ASSISTANCE_TO_PROGRAM = {
    "section8": "section8",
    "srap": "srap",
    "senior_55plus": "age55plus",
    "income_restricted": "income_restricted",
}


def intake_programs(intake: Intake) -> list[str]:
    """Programs a resident qualifies for, derived from their intake."""
    progs: list[str] = []
    mapped = _ASSISTANCE_TO_PROGRAM.get((intake.housing_assistance_type or "").lower())
    if mapped:
        progs.append(mapped)
    # Age 55+ qualifies for senior housing even if they didn't name it.
    if intake.age and intake.age >= 55 and "age55plus" not in progs:
        progs.append("age55plus")
    return progs


def score_listing(intake: Intake, listing: Listing) -> tuple[int, list[str]]:
    """Return (score, reasons) for one listing against one intake.

    Higher = better fit. Program acceptance dominates; location and household
    size are tie-breakers. Every active listing scores at least 1 so nothing is
    silently dropped — poor matches just rank last.
    """
    score = 1
    reasons: list[str] = []

    for prog in intake_programs(intake):
        label, attr = _PROGRAMS[prog]
        if getattr(listing, attr):
            score += 50
            reasons.append(f"Accepts your {label}")

    # Location: resident's stated area matches the listing's city.
    if intake.location and listing.city and listing.city.lower() in intake.location.lower():
        score += 20
        reasons.append(f"In your area ({listing.city})")

    # Household size vs. bedrooms (rough: ~2 people per bedroom).
    if intake.household_size and listing.bedrooms:
        if listing.bedrooms >= max(1, (intake.household_size + 1) // 2):
            score += 10
            reasons.append("Enough bedrooms for your household")

    return score, reasons


def match_listings(
    intake: Intake, listings: list[Listing]
) -> list[tuple[Listing, int, list[str]]]:
    """Score every listing and return them ranked best-fit first."""
    scored = [(lst, *score_listing(intake, lst)) for lst in listings]
    scored.sort(key=lambda row: row[1], reverse=True)  # row[1] = score
    return scored
