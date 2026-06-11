"""Dev-only auth shortcut.

Production auth is Supabase (the frontend gets a real JWT from Supabase, the
backend verifies it). For LOCAL development without a Supabase project, this
endpoint mints a matching HS256 token so the whole flow is demoable. It is
disabled (404) unless DEV_LOGIN_ENABLED is true — keep it false in production.
"""

import time
import uuid

import jwt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


class DevLoginRequest(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: str = "client"


class DevLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


@router.post("/dev-login", response_model=DevLoginResponse)
async def dev_login(body: DevLoginRequest, db: AsyncSession = Depends(get_db)):
    if not settings.DEV_LOGIN_ENABLED:
        raise HTTPException(status_code=404, detail="Not found")

    # Find the user by email, or create one on first dev login.
    user = await db.scalar(select(User).where(User.email == body.email))
    if not user:
        user = User(id=uuid.uuid4(), email=body.email, full_name=body.full_name, role=body.role)
        db.add(user)
    else:
        # Dev convenience: re-login switches role (so the role picker works) / updates name.
        user.role = body.role
        if body.full_name:
            user.full_name = body.full_name
    await db.commit()
    await db.refresh(user)

    # Mint an HS256 token the backend will accept (same secret it verifies with).
    token = jwt.encode(
        {"sub": str(user.id), "exp": int(time.time()) + 60 * 60 * 8},
        settings.hs256_secret,
        algorithm="HS256",
    )
    return DevLoginResponse(access_token=token, user=UserResponse.model_validate(user))
