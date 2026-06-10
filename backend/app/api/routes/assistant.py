"""AI-guided intake assistant endpoints (CC-05 / CC-06).

Public (usable before sign-in). The assistant classifies the need, grounds
answers in HomeMatch's program knowledge, returns real resource matches (search),
and offers the right form to launch next. It only suggests — the resident reviews
and submits the actual intake.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.assistant import (
    ChatRequest,
    ChatResponse,
    ClassifyRequest,
    ClassifyResponse,
)
from app.services.assistant import chat, classify_intent, match_resources, suggest_action

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/classify", response_model=ClassifyResponse)
async def classify(body: ClassifyRequest):
    # CC-06: route a free-text message to a need category + confidence.
    return classify_intent(body.message)


@router.post("/chat", response_model=ChatResponse)
async def assistant_chat(body: ChatRequest, db: AsyncSession = Depends(get_db)):
    # Reply + intent + intake suggestions + program grounding.
    result = await chat([m.model_dump() for m in body.messages])
    last_user = next((m.content for m in reversed(body.messages) if m.role == "user"), "")
    # Search: real resource matches for the need; and the form to launch next.
    result["resources"] = await match_resources(db, result["intent"])
    result["action"] = suggest_action(result["intent"], last_user)
    return result
