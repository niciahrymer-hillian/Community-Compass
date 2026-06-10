"""Schemas for the personalized recommendations feed (CC-33)."""

from typing import List

from pydantic import BaseModel

from app.schemas.listing import ListingMatch
from app.schemas.resource import ResourceResponse


class ResourceRecommendation(BaseModel):
    resource: ResourceResponse
    score: int
    reasons: List[str]


class RecommendationsResponse(BaseModel):
    """One call powers the dashboard: ranked resources + ranked housing."""

    resources: List[ResourceRecommendation]
    housing: List[ListingMatch]
