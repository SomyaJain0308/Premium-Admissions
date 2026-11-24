from uuid import UUID

from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class ApplicantProfile(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "applicant_profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )