from datetime import date
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.user import User

class ApplicantProfile(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "applicant_profiles"

    __table_args__ = (
        CheckConstraint(
            "profile_status IN ('draft', 'complete')",
            name="ck_applicant_profile_status",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    phone_e164: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    profile_status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        server_default="draft",
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="applicant_profile",
    )