"""Pydantic schemas for housing listings (CC-32) and matches (CC-10)."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ListingCreate(BaseModel):
    title: str
    address: str
    city: str
    state: str
    zip: Optional[str] = None
    rent_amount: float
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    section8_accepted: bool = False
    srap_accepted: bool = False
    age_55_plus: bool = False
    income_restricted: bool = False
    lat: Optional[float] = None
    lng: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    description: Optional[str] = None


class ListingResponse(BaseModel):
    id: UUID
    title: str
    address: str
    city: str
    state: str
    zip: Optional[str] = None
    rent_amount: float
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    section8_accepted: bool
    srap_accepted: bool
    age_55_plus: bool
    income_restricted: bool
    lat: Optional[float] = None
    lng: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ListingMatch(BaseModel):
    """A listing plus why/how well it fits the resident's intake (CC-10)."""

    listing: ListingResponse
    score: int
    reasons: List[str]
