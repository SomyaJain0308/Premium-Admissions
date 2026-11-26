from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    display_name: str | None
    avatar_url: str | None
    preferred_locale: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    display_name: str | None = Field(default=None, max_length=160)
    avatar_url: str | None = None
    preferred_locale: str | None = Field(default=None, max_length=20)
