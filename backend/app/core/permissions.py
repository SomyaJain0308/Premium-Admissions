from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.university_membership import UniversityMembership


def require_university_roles(*allowed_roles: str):
    async def check_membership(
        university_id: UUID,
        user_id: UUID = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_db),
    ):
        result = await db.execute(
            select(UniversityMembership).where(
                UniversityMembership.university_id == university_id,
                UniversityMembership.user_id == user_id,
                UniversityMembership.status == "active",
            )
        )

        membership = result.scalar_one_or_none()

        if membership is None or membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this university",
            )

        return membership

    return check_membership