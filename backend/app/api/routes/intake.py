"""Resident intake endpoints (CC-30).

A resident submits their situation here; the saved intake is what risk scoring
and the recommendation engine read later. All routes require auth — the resident
can only create and read their *own* intakes (user_id comes from the token).
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.intake import Intake
from app.models.user import User
from app.schemas.intake import IntakeCreate, IntakeResponse

router = APIRouter(prefix="/intake", tags=["intake"])


@router.post("", response_model=IntakeResponse, status_code=201)
async def create_intake(
    body: IntakeCreate,
    current_user: User = Depends(get_current_user),  # auth → who is submitting
    db: AsyncSession = Depends(get_db),
):
    # Spread the validated fields; force user_id from the token (never the body).
    intake = Intake(user_id=current_user.id, **body.model_dump())
    db.add(intake)
    await db.commit()
    await db.refresh(intake)          # pull DB-populated id/created_at/updated_at
    return IntakeResponse.model_validate(intake)


@router.get("/me", response_model=list[IntakeResponse])
async def list_my_intakes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Newest first so the dashboard shows the latest situation on top.
    result = await db.execute(
        select(Intake)
        .where(Intake.user_id == current_user.id)
        .order_by(Intake.created_at.desc())
    )
    return [IntakeResponse.model_validate(i) for i in result.scalars().all()]


@router.get("/{intake_id}", response_model=IntakeResponse)
async def get_intake(
    intake_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    intake = await db.get(Intake, intake_id)
    # 404 if missing; also 404 (not 403) if it's someone else's — don't reveal it exists.
    if not intake or intake.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Intake not found")
    return IntakeResponse.model_validate(intake)
