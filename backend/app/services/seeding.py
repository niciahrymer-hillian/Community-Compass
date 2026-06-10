"""Synthetic demo data (CC-29).

Populates the catalog the recommendation engine matches against: Delaware
community resources + housing listings. All records are synthetic (real org
*types*, fake contacts/addresses) — no real personal information. Idempotent:
seeds resources/listings only when those tables are empty, so it's safe to run
repeatedly (e.g. on every deploy).
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.listing import Listing
from app.models.resource import Resource

# ── Resources: ~12 across categories, in Delaware cities ────────────────────
SAMPLE_RESOURCES = [
    {"name": "Wilmington Housing Authority", "category": "housing", "need_tags": ["housing"],
     "city": "Wilmington", "state": "DE", "contact_phone": "302-555-0101",
     "website": "https://example.org/wha", "description": "Public housing + voucher intake."},
    {"name": "Sunday Breakfast Mission", "category": "housing", "need_tags": ["housing", "food"],
     "city": "Wilmington", "state": "DE", "contact_phone": "302-555-0102",
     "description": "Emergency shelter and hot meals."},
    {"name": "Food Bank of Delaware", "category": "food", "need_tags": ["food"],
     "city": "Newark", "state": "DE", "contact_phone": "302-555-0103",
     "website": "https://example.org/fbd", "description": "Pantry network + SNAP help."},
    {"name": "DART First State Transit", "category": "transportation", "need_tags": ["transportation"],
     "city": "Dover", "state": "DE", "contact_phone": "302-555-0104",
     "description": "Statewide bus + paratransit; reduced-fare program."},
    {"name": "Delaware JobLink", "category": "employment", "need_tags": ["employment"],
     "city": "Dover", "state": "DE", "contact_phone": "302-555-0105",
     "description": "Job search, training, and workforce development."},
    {"name": "Westside Family Healthcare", "category": "wellness", "need_tags": ["wellness", "health"],
     "city": "Wilmington", "state": "DE", "contact_phone": "302-555-0106",
     "description": "Sliding-scale medical + behavioral health."},
    {"name": "Delaware Center for Justice", "category": "legal_aid", "need_tags": ["safety", "legal_aid"],
     "city": "Wilmington", "state": "DE", "contact_phone": "302-555-0107",
     "description": "Free legal aid and reentry support."},
    {"name": "YMCA Youth Services", "category": "youth_services", "need_tags": ["youth_services", "education"],
     "city": "Newark", "state": "DE", "contact_phone": "302-555-0108",
     "description": "After-school, mentoring, and transition programs."},
    {"name": "Delaware Money School", "category": "financial_literacy", "need_tags": ["financial_literacy"],
     "city": "Dover", "state": "DE", "contact_phone": "302-555-0109",
     "description": "Free budgeting and financial-literacy classes."},
    {"name": "DMV ID & Documents Help", "category": "documents", "need_tags": ["documents"],
     "city": "Dover", "state": "DE", "contact_phone": "302-555-0110",
     "description": "Assistance obtaining state ID and vital records."},
    {"name": "Big Brothers Big Sisters of Delaware", "category": "mentorship", "need_tags": ["mentorship"],
     "city": "Wilmington", "state": "DE", "contact_phone": "302-555-0111",
     "description": "One-to-one youth mentoring."},
    {"name": "Delaware Adult Education (GED)", "category": "education", "need_tags": ["education"],
     "city": "Newark", "state": "DE", "contact_phone": "302-555-0112",
     "description": "Free GED prep and adult basic education."},
]

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
