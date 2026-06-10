"""Resident intake model (CC-30).

One row per intake submission, tied to the resident (User) who made it. These
answers are the input to risk scoring (Future-Path) and the recommendation
engine (housing + resources) built in later cards, so almost every field is
nullable — a resident can save a partial intake and finish later.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Intake(Base):
    __tablename__ = "intakes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # Whose intake this is. ondelete="CASCADE" → deleting a user removes their intakes.
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # ── Situation (CC-04 fields) ────────────────────────────────────────────
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str | None] = mapped_column(String(120), nullable=True)   # city or ZIP
    household_size: Mapped[int | None] = mapped_column(Integer, nullable=True)  # family size
    housing_status: Mapped[str | None] = mapped_column(String(40), nullable=True)   # stable|at_risk|unstable|homeless
    income_range: Mapped[str | None] = mapped_column(String(40), nullable=True)
    employment_status: Mapped[str | None] = mapped_column(String(40), nullable=True)
    education_status: Mapped[str | None] = mapped_column(String(40), nullable=True)
    document_status: Mapped[str | None] = mapped_column(String(40), nullable=True)  # has_id|missing_id|partial

    # ── Need flags (drive risk score + resource matching) ───────────────────
    transportation_need: Mapped[bool] = mapped_column(Boolean, default=False)
    food_access_need: Mapped[bool] = mapped_column(Boolean, default=False)
    health_wellness_need: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_concern: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── Housing eligibility (CC-09) ─────────────────────────────────────────
    # section8 | srap | senior_55plus | income_restricted | none
    housing_assistance_type: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Free text / AI-guided intake summary (CC-05 will populate this).
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    # in_progress (saved draft) | submitted (ready for matching).
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="submitted")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # onupdate → bumped automatically whenever the row changes (e.g. finishing a draft).
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
