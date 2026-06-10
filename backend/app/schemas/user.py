"""Pydantic request/response schemas for users.

Schemas are the API contract: they validate incoming JSON and shape outgoing
JSON. Keeping them separate from the ORM model means we never leak DB-only
fields and can validate input independently of the table.
"""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr   # EmailStr validates the address format


class UserCreate(BaseModel):
    # id comes from Supabase auth (the signed-in user's id), not generated here.
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    # Literal = the request is rejected (422) if role isn't one of these exact values.
    role: Literal["client", "caseworker", "navigator", "volunteer", "admin", "developer"] = "client"


class UserUpdate(BaseModel):
    # Only what a user may change about themselves; all optional (partial update).
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    # The public shape returned to clients — note: no password/secret fields exist to leak.
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    created_at: datetime

    # from_attributes=True → allow building this straight from an ORM User object.
    model_config = {"from_attributes": True}
