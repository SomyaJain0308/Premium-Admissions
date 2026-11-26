from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    
    await db.execute(
        insert(User)
        .values(id=user_id)
        .on_conflict_do_nothing(index_elements=[User.id])
    )
    await db.commit()

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one()