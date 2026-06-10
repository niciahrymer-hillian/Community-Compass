"""Housing listing model (CC-32), trimmed from HomeMatch.

Program-acceptance booleans (section8/srap/55+/income-restricted) are what the
eligibility matcher (CC-10) scores a resident's intake against. lat/lng feed the
interactive map (CC-11).
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    zip: Mapped[str | None] = mapped_column(String(10), nullable=True)
    rent_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)

    # ── Program acceptance (drives eligibility matching, CC-10) ─────────────
    section8_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    srap_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    age_55_plus: Mapped[bool] = mapped_column(Boolean, default=False)
    income_restricted: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── Map coordinates (CC-11) ─────────────────────────────────────────────
    lat: Mapped[float | None] = mapped_column(Numeric(10, 7), nullable=True)
    lng: Mapped[float | None] = mapped_column(Numeric(10, 7), nullable=True)

    # Contact + ownership
    landlord_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    contact_phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
