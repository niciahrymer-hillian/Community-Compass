"""Schemas for the caseworker/navigator dashboard (CC-23 / CC-24)."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.schemas.intake import IntakeResponse
from app.schemas.listing import ListingMatch
from app.schemas.recommendation import ResourceRecommendation
from app.schemas.risk import RiskResponse


class CaseworkerSummary(BaseModel):
    total_residents: int
    high_risk: int
    housing_urgent: int
    missing_documents: int


class ResidentSummary(BaseModel):
    user_id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    housing_status: Optional[str] = None
    location: Optional[str] = None
    risk_score: int
    risk_level: str
    intake_at: datetime


class ResidentProfile(BaseModel):
    user_id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    intake: IntakeResponse
    risk: RiskResponse
    resources: List[ResourceRecommendation]
    housing: List[ListingMatch]
