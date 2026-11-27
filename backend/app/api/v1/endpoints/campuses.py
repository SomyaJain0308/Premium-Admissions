from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_university_roles
from app.models.university_campus import UniversityCampus
from app.models.university_membership import UniversityMembership
from app.schemas.campus import CampusCreate, CampusResponse

router = APIRouter(
    prefix="/universities/{university_id}/campuses",
    tags=["Campuses"],
)


@router.post(
    "/",
    response_model=CampusResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_campus(
    university_id: UUID,
    campus_data: CampusCreate,
    membership: UniversityMembership = Depends(
        require_university_roles("owner", "admin")
    ),
    db: AsyncSession = Depends(get_db),
):
    campus = UniversityCampus(
        university_id=university_id,
        **campus_data.model_dump(),
    )

    db.add(campus)

    try:
        await db.commit()
        await db.refresh(campus)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Campus conflicts with an existing campus",
        )

    return campus


@router.get("/", response_model=list[CampusResponse])
async def get_campuses(
    university_id: UUID,
    membership: UniversityMembership = Depends(
        require_university_roles(
            "owner",
            "admin",
            "admissions_manager",
            "admissions_staff",
            "reviewer",
            "faculty",
            "finance",
        )
    ),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UniversityCampus)
        .where(UniversityCampus.university_id == university_id)
        .order_by(UniversityCampus.created_at)
    )

    return result.scalars().all()