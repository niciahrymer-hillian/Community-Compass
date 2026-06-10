"""Youth risk endpoint (Future-Path engine).

Scores the caller's latest intake using Future-Path's actual risk logic and
returns an explainable result (overall score + level + the factors that drove it).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.intake import Intake
from app.models.user import User
from app.schemas.risk import RiskResponse
from app.services.risk import score_intake

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/me", response_model=RiskResponse)
async def my_risk(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    intake = await db.scalar(
        select(Intake)
        .where(Intake.user_id == current_user.id)
        .order_by(Intake.created_at.desc())
    )
    if not intake:
        raise HTTPException(status_code=400, detail="Complete an intake first")
    return score_intake(intake)
