"""Schemas for the AI-guided intake assistant (CC-05 / CC-06)."""

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class ClassifyRequest(BaseModel):
    message: str


class ClassifyResponse(BaseModel):
    intent: str
    confidence: float


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class IntakeSuggestion(BaseModel):
    """Structured fields the assistant extracted, for the resident to review."""

    housing_status: Optional[str] = None
    housing_assistance_type: Optional[str] = None
    employment_status: Optional[str] = None
    document_status: Optional[str] = None
    transportation_need: Optional[bool] = None
    food_access_need: Optional[bool] = None
    health_wellness_need: Optional[bool] = None
    safety_concern: Optional[bool] = None


class ResourceLink(BaseModel):
    """A real resource the assistant surfaces as a match for the detected need."""

    id: UUID
    name: str
    category: str
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None


class SuggestedAction(BaseModel):
    """A form the assistant offers to launch (e.g. transportation request, youth risk)."""

    kind: Literal["intake", "risk", "housing"]
    label: str
    prefill: dict = {}


class ChatResponse(BaseModel):
    reply: str
    intent: str
    confidence: float
    suggestions: IntakeSuggestion
    # HomeMatch program explanations relevant to the message (grounding).
    program_info: List[str] = []
    # Real resource matches for the detected need (search).
    resources: List[ResourceLink] = []
    # A form to launch next (intake prefill / youth risk / housing).
    action: Optional[SuggestedAction] = None
