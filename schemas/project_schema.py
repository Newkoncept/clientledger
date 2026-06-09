from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

from schemas.client_schema import ClientResponse
from schemas.workspace_schema import WorkSpaceResponse

class ProjectCreateRequest(BaseModel):
    workspace_id: int
    client_id: int
    name: str
    description: Optional[str] = None
    status: str
    start_date: date 
    due_date: date


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None 
    due_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: int
    workspace_id: int
    client_id: int
    name: str
    description: Optional[str] = None
    status: str
    start_date: date 
    due_date: date
    created_at: datetime
    updated_at: datetime



class ProjectFullSummaryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str
    start_date: date 
    due_date: date
    workspace: WorkSpaceResponse
    client: ClientResponse
    created_at: datetime
    updated_at: datetime
