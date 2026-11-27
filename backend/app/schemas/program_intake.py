from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProgramIntakeCreate(BaseModel):
    program_id: UUID
    admission_cycle_id: UUID
    seat_capacity: int = Field(ge=0)
    application_open_at: datetime | None = None
    application_close_at: datetime | None = None


class ProgramIntakeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    university_id: UUID
    program_id: UUID
    admission_cycle_id: UUID
    seat_capacity: int
    application_open_at: datetime | None
    application_close_at: datetime | None
    status: str