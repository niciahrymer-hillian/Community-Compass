"""Pydantic schemas for resident intake (CC-30).

IntakeCreate validates the submission; user_id is taken from the auth token, not
the body, so a resident can only create their own intake.
"""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# Constrained vocabularies → invalid values are rejected with 422 (validation).
HousingStatus = Literal["stable", "at_risk", "unstable", "homeless"]
DocumentStatus = Literal["has_id", "missing_id", "partial"]
AssistanceType = Literal["section8", "srap", "senior_55plus", "income_restricted", "none"]
IntakeStatus = Literal["in_progress", "submitted"]


class IntakeCreate(BaseModel):
    age: Optional[int] = Field(default=None, ge=0, le=120)         # sane bounds
    location: Optional[str] = None
    household_size: Optional[int] = Field(default=None, ge=1, le=30)
    housing_status: Optional[HousingStatus] = None
    income_range: Optional[str] = None
    employment_status: Optional[str] = None
    education_status: Optional[str] = None
    document_status: Optional[DocumentStatus] = None
    transportation_need: bool = False
    food_access_need: bool = False
    health_wellness_need: bool = False
    safety_concern: bool = False
    housing_assistance_type: Optional[AssistanceType] = None
    notes: Optional[str] = None
    status: IntakeStatus = "submitted"


class IntakeResponse(BaseModel):
    id: UUID
    user_id: UUID
    age: Optional[int] = None
    location: Optional[str] = None
    household_size: Optional[int] = None
    housing_status: Optional[str] = None
    income_range: Optional[str] = None
    employment_status: Optional[str] = None
    education_status: Optional[str] = None
    document_status: Optional[str] = None
    transportation_need: bool
    food_access_need: bool
    health_wellness_need: bool
    safety_concern: bool
    housing_assistance_type: Optional[str] = None
    notes: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}   # build straight from the ORM object
