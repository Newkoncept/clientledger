from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime
from typing import Optional
from enum import Enum

from schemas.client_schema import ClientResponse
from schemas.workspace_schema import WorkSpaceResponse


class ProjectStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectCreateRequest(BaseModel):
    workspace_id: int = Field(gt = 0)
    client_id: int = Field(gt = 0)
    name: str = Field(min_length=5, max_length=100)
    description: str | None = None
    status: ProjectStatus
    start_date: date 
    due_date: date

    @model_validator(mode="after")
    def validate_due_date(self):
        if self.due_date < self.start_date:
            raise ValueError("due_date must be greater than start_date")

        return self


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default = None, min_length=5, max_length=100)
    description: str | None = Field(default = None, min_length=5)
    status: ProjectStatus | None = None
    start_date: date | None = None 
    due_date: date | None = None

    @model_validator(mode="after")
    def validate_due_date(self):
        if self.start_date is not None and self.due_date is not None:
            if self.due_date <= self.start_date:
                raise ValueError("due_date must be greater than start_date")

        return self


class ProjectResponse(BaseModel):
    id: int
    workspace_id: int
    client_id: int
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    start_date: date 
    due_date: date
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }



class ProjectFullSummaryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    start_date: date 
    due_date: date
    workspace: WorkSpaceResponse
    client: ClientResponse
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

