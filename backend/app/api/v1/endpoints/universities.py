from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.permissions import require_university_admin, require_university_member
from app.models.university_campus import UniversityCampus
from app.schemas.campus import CampusCreate, CampusResponse
from app.models.university import University
from app.models.university_membership import UniversityMembership
from app.schemas.university import UniversityCreate, UniversityResponse
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.models.program import Program
from app.schemas.program import ProgramCreate, ProgramResponse
from app.models.admission_cycle import AdmissionCycle
from app.schemas.admission_cycle import (
    AdmissionCycleCreate,
    AdmissionCycleResponse,
)
from app.models.program_intake import ProgramIntake
from app.schemas.program_intake import (
    ProgramIntakeCreate,
    ProgramIntakeResponse,
)

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


@router.post(
    "/{university_id}/campuses",
    response_model=CampusResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_campus(
    university_id: UUID,
    campus_data: CampusCreate,
    membership=Depends(require_university_admin),
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
            detail="Campus name, code, or primary campus constraint violated",
        )

    return campus


@router.get(
    "/{university_id}/campuses",
    response_model=list[CampusResponse],
)
async def get_campuses(
    university_id: UUID,
    membership=Depends(require_university_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UniversityCampus)
        .where(UniversityCampus.university_id == university_id)
        .order_by(UniversityCampus.created_at.asc())
    )

    return result.scalars().all()


@router.post(
    "/{university_id}/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    university_id: UUID,
    department_data: DepartmentCreate,
    membership=Depends(require_university_admin),
    db: AsyncSession = Depends(get_db),
):
    department = Department(
        university_id=university_id,
        **department_data.model_dump(),
    )

    db.add(department)

    try:
        await db.commit()
        await db.refresh(department)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department name or code already exists",
        )

    return department


@router.get(
    "/{university_id}/departments",
    response_model=list[DepartmentResponse],
)
async def get_departments(
    university_id: UUID,
    membership=Depends(require_university_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Department)
        .where(Department.university_id == university_id)
        .order_by(Department.name.asc())
    )

    return result.scalars().all()


@router.post(
    "/{university_id}/programs",
    response_model=ProgramResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_program(
    university_id: UUID,
    program_data: ProgramCreate,
    membership=Depends(require_university_admin),
    db: AsyncSession = Depends(get_db),
):
    program = Program(
        university_id=university_id,
        **program_data.model_dump(),
    )

    db.add(program)

    try:
        await db.commit()
        await db.refresh(program)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Program code already exists or department is invalid",
        )

    return program


@router.get(
    "/{university_id}/programs",
    response_model=list[ProgramResponse],
)
async def get_programs(
    university_id: UUID,
    membership=Depends(require_university_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Program)
        .where(Program.university_id == university_id)
        .order_by(Program.name.asc())
    )

    return result.scalars().all()


@router.post(
    "/{university_id}/admission-cycles",
    response_model=AdmissionCycleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_admission_cycle(
    university_id: UUID,
    cycle_data: AdmissionCycleCreate,
    membership=Depends(require_university_admin),
    db: AsyncSession = Depends(get_db),
):
    cycle = AdmissionCycle(
        university_id=university_id,
        **cycle_data.model_dump(),
    )

    db.add(cycle)

    try:
        await db.commit()
        await db.refresh(cycle)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admission cycle name or dates conflict with existing constraints",
        )

    return cycle


@router.get(
    "/{university_id}/admission-cycles",
    response_model=list[AdmissionCycleResponse],
)
async def get_admission_cycles(
    university_id: UUID,
    membership=Depends(require_university_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AdmissionCycle)
        .where(AdmissionCycle.university_id == university_id)
        .order_by(AdmissionCycle.academic_year_start.desc())
    )

    return result.scalars().all()


@router.post(
    "/{university_id}/program-intakes",
    response_model=ProgramIntakeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_program_intake(
    university_id: UUID,
    intake_data: ProgramIntakeCreate,
    membership=Depends(require_university_admin),
    db: AsyncSession = Depends(get_db),
):
    intake = ProgramIntake(
        university_id=university_id,
        **intake_data.model_dump(),
    )

    db.add(intake)

    try:
        await db.commit()
        await db.refresh(intake)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid program, admission cycle, or duplicate intake",
        )

    return intake


@router.get(
    "/{university_id}/program-intakes",
    response_model=list[ProgramIntakeResponse],
)
async def get_program_intakes(
    university_id: UUID,
    membership=Depends(require_university_member),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProgramIntake)
        .where(ProgramIntake.university_id == university_id)
        .order_by(ProgramIntake.created_at.desc())
    )

    return result.scalars().all()