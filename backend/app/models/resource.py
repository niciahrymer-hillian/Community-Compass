"""Community resource model (CC-12).

A verified service a resident can be connected to (shelter, food bank, job
center, clinic, etc.). `need_tags` is what the recommendation engine (CC-13)
matches a resident's intake need-flags against, so it's a searchable list.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import ArrayOfString, Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # Constrained at the schema layer; indexed here because we filter by it a lot.
    category: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    # Tags like ["housing", "food", "transportation"] — matched to intake needs.
    # ArrayOfString = native array in Postgres, JSON on SQLite (portable).
    need_tags: Mapped[list[str]] = mapped_column(ArrayOfString, default=list)

    # ── Contact + location (CC-12) ──────────────────────────────────────────
    contact_phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    state: Mapped[str | None] = mapped_column(String(40), nullable=True)
    eligibility_notes: Mapped[str | None] = mapped_column(String, nullable=True)

    # Soft-delete: admins deactivate stale resources instead of deleting them,
    # so default listings hide them but history/links stay intact.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
