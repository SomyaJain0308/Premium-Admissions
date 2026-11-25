from datetime import date
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class AdmissionCycle(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "admission_cycles"

    __table_args__ = (
        UniqueConstraint(
            "university_id", "name",
            name="uq_university_admission_cycle",
        ),
        UniqueConstraint(
            "id", "university_id",
            name="uq_cycle_id_university",
        ),
        CheckConstraint(
            "application_end_date > application_start_date",
            name="ck_cycle_application_dates",
        ),
        CheckConstraint(
            "academic_year_end > academic_year_start",
            name="ck_cycle_academic_dates",
        ),
        CheckConstraint(
            "status IN ('draft', 'open', 'closed', 'archived')",
            name="ck_admission_cycle_status",
        ),
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    application_start_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    application_end_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    academic_year_start: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    academic_year_end: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        server_default="draft",
        nullable=False,
    )