from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class Program(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "programs"

    __table_args__ = (
        UniqueConstraint(
            "university_id", "code",
            name="uq_university_program_code",
        ),
        UniqueConstraint(
            "id", "university_id",
            name="uq_program_id_university",
        ),
        CheckConstraint(
            "degree_level IN ('certificate', 'diploma', "
            "'undergraduate', 'postgraduate', 'doctoral')",
            name="ck_program_degree_level",
        ),
        CheckConstraint(
            "duration_months > 0",
            name="ck_program_duration",
        ),
        CheckConstraint(
            "status IN ('active', 'inactive', 'archived')",
            name="ck_program_status",
        ),
        CheckConstraint(
            "delivery_mode IN ('on_campus', 'online', 'hybrid')",
            name="ck_program_delivery_mode",
        ),
        ForeignKeyConstraint(
            ["department_id", "university_id"],
            ["departments.id", "departments.university_id"],
            name="fk_program_department_university",
            ondelete="RESTRICT",
        ),
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    department_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    degree_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    degree_level: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    duration_months: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    delivery_mode: Mapped[str] = mapped_column(
        String(30),
        default="on_campus",
        server_default="on_campus",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        server_default="active",
        nullable=False,
    )