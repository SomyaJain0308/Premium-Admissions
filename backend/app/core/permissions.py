from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.university_membership import UniversityMembership


async def require_university_admin(
    university_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> UniversityMembership:

    result = await db.execute(
        select(UniversityMembership).where(
            UniversityMembership.university_id == university_id,
            UniversityMembership.user_id == user_id,
            UniversityMembership.status == "active",
        )
    )

    membership = result.scalar_one_or_none()

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="University not found",
        )

    if membership.role not in {"owner", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return membership


async def require_university_member(
    university_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> UniversityMembership:

    result = await db.execute(
        select(UniversityMembership).where(
            UniversityMembership.university_id == university_id,
            UniversityMembership.user_id == user_id,
            UniversityMembership.status == "active",
        )
    )

    membership = result.scalar_one_or_none()

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="University not found",
        )

    return membership