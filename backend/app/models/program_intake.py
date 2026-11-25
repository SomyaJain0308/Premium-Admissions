from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class ProgramIntake(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "program_intakes"

    __table_args__ = (
        ForeignKeyConstraint(
            ["program_id", "university_id"],
            ["programs.id", "programs.university_id"],
            ondelete="CASCADE",
            name="fk_intake_program_university",
        ),
        ForeignKeyConstraint(
            ["admission_cycle_id", "university_id"],
            [
                "admission_cycles.id",
                "admission_cycles.university_id",
            ],
            ondelete="CASCADE",
            name="fk_intake_cycle_university",
        ),
        UniqueConstraint(
            "program_id",
            "admission_cycle_id",
            name="uq_program_cycle",
        ),
        CheckConstraint(
            "seat_capacity >= 0",
            name="ck_intake_seat_capacity",
        ),
        CheckConstraint(
            "status IN ('draft', 'open', 'closed', 'paused')",
            name="ck_program_intake_status",
        ),
        CheckConstraint(
            "application_close_at IS NULL OR "
            "application_open_at IS NULL OR "
            "application_close_at > application_open_at",
            name="ck_intake_application_dates",
        ),
        Index(
            "ix_intakes_university_status",
            "university_id",
            "status",
        ),
    )

    university_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    program_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    admission_cycle_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    seat_capacity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    application_open_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    application_close_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        server_default="draft",
        nullable=False,
    )