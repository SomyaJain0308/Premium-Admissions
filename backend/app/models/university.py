from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

class University(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "universities"

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'active', 'suspended', 'archived')",
            name="ck_university_status",
        ),
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    website_url: Mapped[str | None] = mapped_column(
        Text,
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

    currency_code: Mapped[str] = mapped_column(
        String(3),
        default="INR",
        server_default="INR",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        server_default="draft",
        nullable=False,
    )

    programs: Mapped[list["Program"]] = relationship(
        back_populates="university",
        cascade="all, delete-orphan",
    )

    memberships: Mapped[list["UniversityMembership"]] = relationship(
        back_populates="university",
    )