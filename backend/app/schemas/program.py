from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProgramCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    code: str = Field(min_length=2, max_length=50)
    degree_name: str = Field(min_length=2, max_length=100)
    degree_level: str
    description: str | None = None
    duration_months: int = Field(gt=0)
    delivery_mode: str = "on_campus"
    department_id: UUID | None = None


class ProgramResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    university_id: UUID
    department_id: UUID | None
    name: str
    code: str
    degree_name: str
    degree_level: str
    description: str | None
    duration_months: int
    delivery_mode: str
    status: str