"""Schemas for the youth risk score (Future-Path engine)."""

from typing import List

from pydantic import BaseModel


class RiskFactor(BaseModel):
    name: str
    score: int
    reason: str


class RiskResponse(BaseModel):
    score: int            # 0–100
    level: str            # Low | Medium | High
    factors: List[RiskFactor]
