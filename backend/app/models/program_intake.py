from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class ProgramIntake(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "program_intakes"

    __table_args__ = (
        UniqueConstraint(
            "program_id",
            "admission_cycle_id",
            name="uq_program_cycle",
        ),
    )

    program_id: Mapped[UUID] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"),
        nullable=False,
    )

    admission_cycle_id: Mapped[UUID] = mapped_column(
        ForeignKey("admission_cycles.id", ondelete="CASCADE"),
        nullable=False,
    )

    total_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reserved_seats: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )