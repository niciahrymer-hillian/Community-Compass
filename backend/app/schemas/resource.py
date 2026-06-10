"""Pydantic schemas for community resources (CC-12 / CC-31)."""

from datetime import datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

# Category vocabulary (CC-12 + user-story #5). Invalid category → 422.
ResourceCategory = Literal[
    "housing",
    "food",
    "employment",
    "transportation",
    "education",
    "wellness",
    "documents",
    "safety",
    "youth_services",
    "financial_literacy",
    "legal_aid",
    "mentorship",
]


class ResourceCreate(BaseModel):
    name: str
    category: ResourceCategory
    description: Optional[str] = None
    need_tags: List[str] = []
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    eligibility_notes: Optional[str] = None


class ResourceUpdate(BaseModel):
    # All optional → partial update (PUT applies only the fields sent).
    name: Optional[str] = None
    category: Optional[ResourceCategory] = None
    description: Optional[str] = None
    need_tags: Optional[List[str]] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    eligibility_notes: Optional[str] = None
    is_active: Optional[bool] = None


class ResourceResponse(BaseModel):
    id: UUID
    name: str
    category: str
    description: Optional[str] = None
    need_tags: List[str] = []
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    eligibility_notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
