"""User model. The id matches the Supabase auth user id (one row per account).

Kept lean for the foundation — identity + role only. Intake answers, risk
scores, and housing profile live in their own models (added in later PRs), so
this table stays stable as those features land.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.dialects.postgresql import UUID      # renders as native uuid in PG, CHAR on SQLite
from sqlalchemy.orm import Mapped, mapped_column     # 2.0 typed-column style
from sqlalchemy.sql import func                       # func.now() = DB-side timestamp

from app.core.database import Base

# Allowed roles (user-story #13 / CC-25). "client" = a person seeking housing/support;
# "caseworker"/"navigator" are support staff. Kept as a constant for schemas/tests.
ROLES = ("client", "caseworker", "navigator", "volunteer", "admin", "developer")


class User(Base):
    __tablename__ = "users"   # table name in the database

    # Primary key IS the Supabase auth user id (default only used for non-auth test rows).
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # unique=True → DB rejects duplicate accounts for the same email.
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)  # optional display name
    # default="client" applies when a row is created without an explicit role.
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="client")
    # server_default=func.now() → the DATABASE stamps the time on insert (not Python).
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        # Enforce the role whitelist at the DB level too — defense in depth beyond
        # the Pydantic Literal, so bad data can't sneak in via raw SQL/migrations.
        CheckConstraint(
            "role IN ('client', 'caseworker', 'navigator', 'volunteer', 'admin', 'developer')",
            name="ck_users_role",
        ),
    )
