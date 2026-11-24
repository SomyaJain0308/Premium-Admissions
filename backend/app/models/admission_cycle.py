from uuid import UUID
from datetime import date

from sqlalchemy import String, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class AdmissionCycle(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "admission_cycles"

    __table_args__ = (
        UniqueConstraint(
            "university_id",
            "name",
            name="uq_university_admission_cycle",
        ),
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    application_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    application_end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    academic_year_start: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    academic_year_end: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="draft",
        nullable=False,
    )