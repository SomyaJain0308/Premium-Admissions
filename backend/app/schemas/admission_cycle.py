from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AdmissionCycleCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    application_start_date: date
    application_end_date: date
    academic_year_start: date
    academic_year_end: date


class AdmissionCycleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    university_id: UUID
    name: str
    application_start_date: date
    application_end_date: date
    academic_year_start: date
    academic_year_end: date
    status: str