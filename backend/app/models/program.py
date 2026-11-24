from uuid import UUID

from sqlalchemy import String, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class Program(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "programs"

    __table_args__ = (
        UniqueConstraint(
            "university_id",
            "code",
            name="uq_university_program_code",
        ),
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    degree: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    duration_years: Mapped[int] = mapped_column(
        nullable=False,
    )