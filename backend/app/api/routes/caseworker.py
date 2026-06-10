"""Caseworker / navigator dashboard (CC-23) + resident profile (CC-24).

Support staff (caseworker/navigator/admin) see residents ranked by risk, filter
by risk level, and open a full profile (intake + Future-Path risk + matched
resources/housing). Read-only over residents' own intakes.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_caseworker
from app.models.intake import Intake
from app.models.listing import Listing
from app.models.resource import Resource
from app.models.user import User
from app.schemas.caseworker import CaseworkerSummary, ResidentProfile, ResidentSummary
from app.schemas.intake import IntakeResponse
from app.schemas.listing import ListingMatch, ListingResponse
from app.schemas.recommendation import ResourceRecommendation
from app.schemas.resource import ResourceResponse
from app.schemas.risk import RiskResponse
from app.services.eligibility import match_listings
from app.services.recommender import recommend_resources
from app.services.risk import score_intake

router = APIRouter(prefix="/caseworker", tags=["caseworker"])


async def _latest_intakes(db: AsyncSession) -> dict[UUID, Intake]:
    """Most recent intake per resident (newest-first scan, first wins)."""
    rows = (await db.scalars(select(Intake).order_by(Intake.created_at.desc()))).all()
    latest: dict[UUID, Intake] = {}
    for i in rows:
        latest.setdefault(i.user_id, i)
    return latest


@router.get("/summary", response_model=CaseworkerSummary)
async def summary(
    _staff: User = Depends(get_current_caseworker),
    db: AsyncSession = Depends(get_db),
):
    latest = await _latest_intakes(db)
    high = housing_urgent = missing_docs = 0
    for intake in latest.values():
        if score_intake(intake)["level"] == "High":
            high += 1
        if (intake.housing_status or "") in ("homeless", "unstable"):
            housing_urgent += 1
        if (intake.document_status or "") == "missing_id":
            missing_docs += 1
    return CaseworkerSummary(
        total_residents=len(latest),
        high_risk=high,
        housing_urgent=housing_urgent,
        missing_documents=missing_docs,
    )


@router.get("/residents", response_model=list[ResidentSummary])
async def residents(
    risk: Optional[str] = None,                     # filter by level: Low | Medium | High
    _staff: User = Depends(get_current_caseworker),
    db: AsyncSession = Depends(get_db),
):
    latest = await _latest_intakes(db)
    if not latest:
        return []
    users = {
        u.id: u
        for u in (await db.scalars(select(User).where(User.id.in_(latest.keys())))).all()
    }
    out: list[ResidentSummary] = []
    for uid, intake in latest.items():
        u = users.get(uid)
        if not u:
            continue
        r = score_intake(intake)
        if risk and r["level"].lower() != risk.lower():
            continue
        out.append(ResidentSummary(
            user_id=uid, email=u.email, full_name=u.full_name,
            housing_status=intake.housing_status, location=intake.location,
            risk_score=r["score"], risk_level=r["level"], intake_at=intake.created_at,
        ))
    out.sort(key=lambda x: x.risk_score, reverse=True)   # most urgent first
    return out


@router.get("/residents/{user_id}", response_model=ResidentProfile)
async def resident_profile(
    user_id: UUID,
    _staff: User = Depends(get_current_caseworker),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Resident not found")
    intake = await db.scalar(
        select(Intake).where(Intake.user_id == user_id).order_by(Intake.created_at.desc())
    )
    if not intake:
        raise HTTPException(status_code=404, detail="Resident has no intake")

    resources = (await db.scalars(select(Resource).where(Resource.is_active.is_(True)))).all()
    listings = (await db.scalars(select(Listing).where(Listing.is_active.is_(True)))).all()
    recs = [
        ResourceRecommendation(resource=ResourceResponse.model_validate(res), score=s, reasons=rs)
        for res, s, rs in recommend_resources(intake, list(resources))
    ]
    housing = [
        ListingMatch(listing=ListingResponse.model_validate(lst), score=s, reasons=rs)
        for lst, s, rs in match_listings(intake, list(listings)) if s > 1
    ][:5]
    return ResidentProfile(
        user_id=user.id, email=user.email, full_name=user.full_name, role=user.role,
        intake=IntakeResponse.model_validate(intake),
        risk=RiskResponse(**score_intake(intake)),
        resources=recs, housing=housing,
    )
