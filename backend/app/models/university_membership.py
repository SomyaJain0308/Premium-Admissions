from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class UniversityMembership(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "university_memberships"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "university_id",
            name="uq_user_university",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="admissions_staff",
    )