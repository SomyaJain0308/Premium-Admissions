from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UniversityCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    legal_name: str | None = Field(default=None, max_length=255)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    website_url: HttpUrl | None = None
    country_code: str = Field(default="IN", min_length=2, max_length=2)
    timezone: str = "Asia/Kolkata"
    currency_code: str = Field(default="INR", min_length=3, max_length=3)


class UniversityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    status: str
    created_at: datetime