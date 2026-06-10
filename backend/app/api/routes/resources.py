"""Community resource endpoints (CC-31).

Reads are public (residents browse/search without logging in). Writes are
admin-only (CC-22 resource management) via the get_current_admin guard.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.resource import Resource
from app.models.user import User
from app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceResponse])
async def list_resources(
    db: AsyncSession = Depends(get_db),
    category: Optional[str] = None,                 # filter by category
    city: Optional[str] = None,                     # filter by city
    q: Optional[str] = Query(default=None),         # keyword search (name/description)
    active_only: bool = True,                       # hide deactivated by default
):
    stmt = select(Resource)
    if active_only:
        stmt = stmt.where(Resource.is_active.is_(True))
    if category:
        stmt = stmt.where(Resource.category == category)
    if city:
        stmt = stmt.where(Resource.city == city)
    if q:
        # ilike → case-insensitive contains; search name OR description.
        like = f"%{q}%"
        stmt = stmt.where(or_(Resource.name.ilike(like), Resource.description.ilike(like)))
    stmt = stmt.order_by(Resource.name)
    result = await db.execute(stmt)
    return [ResourceResponse.model_validate(r) for r in result.scalars().all()]


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceResponse.model_validate(resource)


@router.post("", response_model=ResourceResponse, status_code=201)
async def create_resource(
    body: ResourceCreate,
    _admin: User = Depends(get_current_admin),       # admin-only
    db: AsyncSession = Depends(get_db),
):
    resource = Resource(**body.model_dump())
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return ResourceResponse.model_validate(resource)


@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: UUID,
    body: ResourceUpdate,
    _admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    resource = await db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    # Apply only the fields the admin actually sent.
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    await db.commit()
    await db.refresh(resource)
    return ResourceResponse.model_validate(resource)


@router.post("/{resource_id}/deactivate", response_model=ResourceResponse)
async def deactivate_resource(
    resource_id: UUID,
    _admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    resource = await db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource.is_active = False        # soft-delete, keeps the record
    await db.commit()
    await db.refresh(resource)
    return ResourceResponse.model_validate(resource)
