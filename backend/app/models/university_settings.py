from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from app.models.base import Base, TimestampMixin


class UniversitySettings(TimestampMixin, Base):
    __tablename__ = "university_settings"

    university_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("universities.id", ondelete="CASCADE"),
        primary_key=True,
    )

    logo_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    favicon_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    primary_color: Mapped[str | None] = mapped_column(
        String(7),
        nullable=True,
    )

    secondary_color: Mapped[str | None] = mapped_column(
        String(7),
        nullable=True,
    )

    custom_domain: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    applicant_portal_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    welcome_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    default_locale: Mapped[str] = mapped_column(
        String(20),
        default="en-IN",
        server_default="en-IN",
        nullable=False,
    )