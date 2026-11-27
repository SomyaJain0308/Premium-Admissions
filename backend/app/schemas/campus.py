from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CampusCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    code: str | None = Field(default=None, max_length=30)
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state_region: str | None = None
    postal_code: str | None = None
    country_code: str = Field(default="IN", min_length=2, max_length=2)
    timezone: str = "Asia/Kolkata"
    is_primary: bool = False


class CampusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    university_id: UUID
    name: str
    code: str | None
    city: str | None
    country_code: str
    is_primary: bool
    status: str