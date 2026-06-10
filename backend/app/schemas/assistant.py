"""Schemas for the AI-guided intake assistant (CC-05 / CC-06)."""

from typing import List, Literal, Optional

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


class ChatResponse(BaseModel):
    reply: str
    intent: str
    confidence: float
    suggestions: IntakeSuggestion
    # HomeMatch program explanations relevant to the message (grounding).
    program_info: List[str] = []
