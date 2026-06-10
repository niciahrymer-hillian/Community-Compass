"""Consolidated newsfeed endpoint (CC-15): FirstStep items + live HUD/DSHA."""

from fastapi import APIRouter

from app.services.news import get_news

router = APIRouter(tags=["news"])


@router.get("/news")
async def news() -> list[dict]:
    return await get_news()
