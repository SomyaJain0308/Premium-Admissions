from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class UniversityCampus(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "university_campuses"

    __table_args__ = (
        UniqueConstraint(
            "university_id",
            "name",
            name="uq_university_campus_name",
        ),
        UniqueConstraint(
            "university_id",
            "code",
            name="uq_university_campus_code",
        ),
        CheckConstraint(
            "status IN ('active', 'inactive')",
            name="ck_campus_status",
        ),
        Index(
            "uq_university_primary_campus",
            "university_id",
            unique=True,
            postgresql_where=text("is_primary IS TRUE"),
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

    code: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    address_line_1: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state_region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        default="IN",
        server_default="IN",
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(64),
        default="Asia/Kolkata",
        server_default="Asia/Kolkata",
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        server_default="active",
        nullable=False,
    )