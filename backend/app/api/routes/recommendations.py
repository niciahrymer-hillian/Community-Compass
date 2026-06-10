"""Personalized recommendations (CC-33).

One endpoint the resident dashboard (CC-07) calls: it reads the caller's latest
intake and returns ranked resource recommendations + ranked housing matches,
each with reasons. Pure read of existing data — no auth role beyond being signed in.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.intake import Intake
from app.models.listing import Listing
from app.models.resource import Resource
from app.models.user import User
from app.schemas.listing import ListingResponse, ListingMatch
from app.schemas.recommendation import RecommendationsResponse, ResourceRecommendation
from app.schemas.resource import ResourceResponse
from app.services.eligibility import match_listings
from app.services.recommender import recommend_resources

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/me", response_model=RecommendationsResponse)
async def my_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Base everything on the resident's most recent intake.
    intake = await db.scalar(
        select(Intake)
        .where(Intake.user_id == current_user.id)
        .order_by(Intake.created_at.desc())
    )
    if not intake:
        raise HTTPException(status_code=400, detail="Complete an intake first")

    # Resource recommendations (rules recommender).
    active_resources = (
        await db.scalars(select(Resource).where(Resource.is_active.is_(True)))
    ).all()
    resource_recs = [
        ResourceRecommendation(
            resource=ResourceResponse.model_validate(res), score=score, reasons=reasons
        )
        for res, score, reasons in recommend_resources(intake, list(active_resources))
    ]

    # Housing matches (eligibility engine); keep the top few for the dashboard.
    active_listings = (
        await db.scalars(select(Listing).where(Listing.is_active.is_(True)))
    ).all()
    housing = [
        ListingMatch(listing=ListingResponse.model_validate(lst), score=score, reasons=reasons)
        for lst, score, reasons in match_listings(intake, list(active_listings))
        if score > 1  # only show listings that actually fit, not every row
    ][:5]

    return RecommendationsResponse(resources=resource_recs, housing=housing)
