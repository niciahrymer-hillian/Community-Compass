"""User profile endpoints.

Supabase handles sign-up/sign-in; the frontend then calls POST /users/register
once to create the matching profile row, using the Supabase user id. /me reads
and updates the current (token-authenticated) user.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

# prefix → every path here starts with /users; tags → groups them in the docs.
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    # body.id is the Supabase user id — reject if a profile already exists for it.
    if await db.get(User, body.id):
        raise HTTPException(status_code=409, detail="User already exists")
    user = User(id=body.id, email=body.email, full_name=body.full_name, role=body.role)
    db.add(user)                 # stage the insert
    await db.commit()            # write it
    await db.refresh(user)       # reload DB-populated fields (created_at) onto the object
    return UserResponse.model_validate(user)  # serialize via the response schema


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    # get_current_user already verified the token and loaded the row — just return it.
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),   # auth + the row to mutate
    db: AsyncSession = Depends(get_db),
):
    # exclude_none → only overwrite fields the client actually sent (partial update).
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)
