"""Liveness probe — also the Render healthCheckPath."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    # Render pings this to know the service is up; keep it dependency-free
    # (no DB call) so it stays green even if the database is briefly unavailable.
    return {"status": "ok"}
