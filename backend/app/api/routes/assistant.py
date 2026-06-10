"""AI-guided intake assistant endpoints (CC-05 / CC-06).

Public (usable before sign-in, while exploring). The assistant only suggests
structured intake fields — the resident reviews and submits the actual intake.
"""

from fastapi import APIRouter

from app.schemas.assistant import (
    ChatRequest,
    ChatResponse,
    ClassifyRequest,
    ClassifyResponse,
)
from app.services.assistant import chat, classify_intent

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/classify", response_model=ClassifyResponse)
async def classify(body: ClassifyRequest):
    # CC-06: route a free-text message to a need category + confidence.
    return classify_intent(body.message)


@router.post("/chat", response_model=ChatResponse)
async def assistant_chat(body: ChatRequest):
    # CC-05: conversational reply + structured intake suggestions to review.
    return await chat([m.model_dump() for m in body.messages])
