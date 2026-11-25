from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.university import University    
from app.models.user import User

class UniversityMembership(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "university_memberships"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "university_id",
            name="uq_user_university",
        ),
        CheckConstraint(
            "role IN ('owner', 'admin', 'admissions_manager', "
            "'admissions_staff', 'reviewer', 'faculty', 'finance')",
            name="ck_university_membership_role",
        ),
        CheckConstraint(
            "status IN ('invited', 'active', 'suspended', 'revoked')",
            name="ck_university_membership_status",
        ),
        Index(
            "ix_memberships_university_status",
            "university_id",
            "status",
        ),
    )

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
            name="fk_membership_invited_by_user",
        ),
        nullable=False,
    )

    university_id: Mapped[UUID] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="admissions_staff",
        server_default="admissions_staff",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="invited",
        server_default="invited",
    )

    invited_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    invited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="memberships",
    )

    university: Mapped["University"] = relationship(
        back_populates="memberships",
    )