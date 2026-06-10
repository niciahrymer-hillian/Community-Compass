"""Demo data (CC-29).

Resources are REAL Delaware records imported from FirstStep
(app/data/firststep_resources.json — 58 verified orgs across housing, clothing,
and household assistance; credit: FirstStep / gitanitraj). Housing listings stay
synthetic (no real rental inventory with coordinates available yet). Idempotent:
seeds a table only when it's empty, so it's safe to run repeatedly.
"""

import json
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.listing import Listing
from app.models.resource import Resource

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "firststep_resources.json"

# FirstStep category → our resource category vocabulary.
_CATEGORY_MAP = {
    "Housing Assistance": "housing",
    "Clothing & Incidentals": "clothing",
    "Furniture & Household Items": "household",
}


def _map_firststep(r: dict) -> dict:
    """Map one FirstStep resource record onto our Resource columns."""
    loc = (r.get("locations") or [{}])[0]
    phone = (r.get("phones") or [{}])[0].get("number")
    website = (r.get("websites") or [{}])[0].get("url")
    population = r.get("population")
    notes = "; ".join(
        x for x in [r.get("eligibility"),
                    f"Population: {population}" if population and population != "All" else None]
        if x
    ) or None
    return {
        "name": (r.get("organization") or r.get("summary") or "Resource")[:200],
        "category": _CATEGORY_MAP.get(r.get("category"), "housing"),
        "description": r.get("description") or r.get("summary"),
        "need_tags": [t.lower() for t in (r.get("tags") or [])][:8],
        "contact_phone": phone,
        "website": website,
        "address": loc.get("address"),
        "city": loc.get("city"),
        "state": loc.get("state"),
        "eligibility_notes": notes,
    }


def _load_resources() -> list[dict]:
    raw = json.loads(_DATA_FILE.read_text())
    records = raw.get("records", raw) if isinstance(raw, dict) else raw
    return [_map_firststep(r) for r in records]


# 58 real Delaware resources, mapped at import time.
SAMPLE_RESOURCES = _load_resources()

# ── Listings: ~6 with program flags + real-ish DE coordinates ───────────────
SAMPLE_LISTINGS = [
    {"title": "Riverside Apartments", "address": "100 Riverside Dr", "city": "Wilmington", "state": "DE",
     "rent_amount": 950, "bedrooms": 2, "bathrooms": 1, "section8_accepted": True,
     "lat": 39.7459, "lng": -75.5466, "contact_phone": "302-555-0201"},
    {"title": "Dover Senior Living", "address": "55 Loockerman St", "city": "Dover", "state": "DE",
     "rent_amount": 800, "bedrooms": 1, "bathrooms": 1, "age_55_plus": True,
     "lat": 39.1582, "lng": -75.5244, "contact_phone": "302-555-0202"},
    {"title": "Newark Income-Restricted Lofts", "address": "20 Main St", "city": "Newark", "state": "DE",
     "rent_amount": 1100, "bedrooms": 2, "bathrooms": 1, "income_restricted": True,
     "lat": 39.6837, "lng": -75.7497, "contact_phone": "302-555-0203"},
    {"title": "Market Street Flats", "address": "400 Market St", "city": "Wilmington", "state": "DE",
     "rent_amount": 1600, "bedrooms": 1, "bathrooms": 1,
     "lat": 39.7447, "lng": -75.5484, "contact_phone": "302-555-0204"},
    {"title": "Middletown SRAP Townhomes", "address": "8 Cedar Ln", "city": "Middletown", "state": "DE",
     "rent_amount": 1000, "bedrooms": 3, "bathrooms": 2, "srap_accepted": True,
     "lat": 39.4496, "lng": -75.7163, "contact_phone": "302-555-0205"},
    {"title": "Garfield Park Homes", "address": "12 Garfield Ave", "city": "Wilmington", "state": "DE",
     "rent_amount": 875, "bedrooms": 2, "bathrooms": 1, "section8_accepted": True,
     "income_restricted": True, "lat": 39.7298, "lng": -75.5712, "contact_phone": "302-555-0206"},
]


async def _is_empty(db: AsyncSession, model) -> bool:
    count = await db.scalar(select(func.count()).select_from(model))
    return (count or 0) == 0


async def seed_demo(db: AsyncSession) -> dict[str, int]:
    """Insert demo resources/listings if their tables are empty. Returns counts added."""
    added = {"resources": 0, "listings": 0}

    if await _is_empty(db, Resource):
        db.add_all(Resource(**row) for row in SAMPLE_RESOURCES)
        added["resources"] = len(SAMPLE_RESOURCES)

    if await _is_empty(db, Listing):
        db.add_all(Listing(**row) for row in SAMPLE_LISTINGS)
        added["listings"] = len(SAMPLE_LISTINGS)

    await db.commit()
    return added
