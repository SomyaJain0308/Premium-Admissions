from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class Department(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "departments"

    __table_args__ = (
        UniqueConstraint(
            "id",
            "university_id",
            name="uq_department_id_university",
        ),
        UniqueConstraint(
            "university_id",
            "code",
            name="uq_university_department_code",
        ),
        UniqueConstraint(
            "university_id",
            "name",
            name="uq_university_department_name",
        ),
        CheckConstraint(
            "status IN ('active', 'inactive', 'archived')",
            name="ck_department_status",
        ),
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        server_default="active",
        nullable=False,
    )