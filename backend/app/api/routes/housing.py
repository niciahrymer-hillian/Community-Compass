"""Housing listing + eligibility-match endpoints (CC-32 / CC-10).

Browsing listings is public; creating them is admin-only for now (landlord role
comes later). /housing/matches ranks listings against the caller's own intake.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin, get_current_user
from app.models.intake import Intake
from app.models.listing import Listing
from app.models.user import User
from app.schemas.listing import ListingCreate, ListingMatch, ListingResponse
from app.services.eligibility import match_listings

router = APIRouter(prefix="/housing", tags=["housing"])

# program query value → the Listing boolean column to filter on.
_PROGRAM_COLUMN = {
    "section8": Listing.section8_accepted,
    "srap": Listing.srap_accepted,
    "age55plus": Listing.age_55_plus,
    "income_restricted": Listing.income_restricted,
}


@router.get("", response_model=list[ListingResponse])
async def list_listings(
    db: AsyncSession = Depends(get_db),
    city: Optional[str] = None,
    program: Optional[str] = None,          # section8 | srap | age55plus | income_restricted
    max_rent: Optional[float] = None,
    bedrooms: Optional[int] = None,         # minimum bedrooms
    active_only: bool = True,
):
    stmt = select(Listing)
    if active_only:
        stmt = stmt.where(Listing.is_active.is_(True))
    if city:
        stmt = stmt.where(Listing.city == city)
    if program and program in _PROGRAM_COLUMN:
        stmt = stmt.where(_PROGRAM_COLUMN[program].is_(True))
    if max_rent is not None:
        stmt = stmt.where(Listing.rent_amount <= max_rent)
    if bedrooms is not None:
        stmt = stmt.where(Listing.bedrooms >= bedrooms)
    stmt = stmt.order_by(Listing.rent_amount)
    result = await db.execute(stmt)
    return [ListingResponse.model_validate(x) for x in result.scalars().all()]


@router.get("/matches", response_model=list[ListingMatch])
async def my_matches(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Use the resident's most recent intake as the basis for matching.
    intake = await db.scalar(
        select(Intake)
        .where(Intake.user_id == current_user.id)
        .order_by(Intake.created_at.desc())
    )
    if not intake:
        raise HTTPException(status_code=400, detail="Complete an intake first")

    listings = (
        await db.scalars(select(Listing).where(Listing.is_active.is_(True)))
    ).all()
    ranked = match_listings(intake, list(listings))
    return [
        ListingMatch(listing=ListingResponse.model_validate(lst), score=score, reasons=reasons)
        for lst, score, reasons in ranked
    ]


@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: UUID, db: AsyncSession = Depends(get_db)):
    listing = await db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return ListingResponse.model_validate(listing)


@router.post("", response_model=ListingResponse, status_code=201)
async def create_listing(
    body: ListingCreate,
    _admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    listing = Listing(**body.model_dump())
    db.add(listing)
    await db.commit()
    await db.refresh(listing)
    return ListingResponse.model_validate(listing)
