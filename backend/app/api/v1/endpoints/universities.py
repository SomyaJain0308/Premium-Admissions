from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.university import University
from app.models.university_membership import UniversityMembership
from app.schemas.university import UniversityCreate, UniversityResponse

router = APIRouter(prefix="/universities", tags=["Universities"])


@router.post(
    "/",
    response_model=UniversityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_university(
    university_data: UniversityCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(
        select(University).where(
            University.slug == university_data.slug
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="University slug already exists",
        )

    university = University(
        **university_data.model_dump(exclude={"website_url"}),
        website_url=(
            str(university_data.website_url)
            if university_data.website_url
            else None
        ),
    )

    db.add(university)

    try:
        await db.flush()

        membership = UniversityMembership(
            user_id=user_id,
            university_id=university.id,
            role="owner",
            status="active",
        )

        db.add(membership)

        await db.commit()
        await db.refresh(university)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="University could not be created due to conflicting data",
        )

    return university


@router.get("/", response_model=list[UniversityResponse])
async def get_my_universities(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(University)
        .join(
            UniversityMembership,
            UniversityMembership.university_id == University.id,
        )
        .where(
            UniversityMembership.user_id == user_id,
            UniversityMembership.status == "active",
        )
        .order_by(University.created_at.desc())
    )

    return result.scalars().all()