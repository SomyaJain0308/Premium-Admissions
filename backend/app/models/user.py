from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "auth.users.id",
            ondelete="CASCADE",
            name="fk_users_auth_user_id",
        ),
        primary_key=True,
    )

    display_name: Mapped[str | None] = mapped_column(
        String(160),
        nullable=True,
    )

    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    preferred_locale: Mapped[str] = mapped_column(
        String(20),
        default="en-IN",
        server_default="en-IN",
        nullable=False,
    )