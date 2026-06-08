from pydantic import BaseModel, Field
from datetime import datetime

from schemas.workspacemember_schema import WorkspaceMemberResponse

class WorkSpaceRequest(BaseModel):
    name: str = Field(min_length= 5, max_length = 100)


class WorkSpaceResponse(BaseModel):
    id: int
    name: str
    owner_id: int 
    created_at: datetime
    updated_at: datetime


class WorkspaceFullResponse(BaseModel):
    workspace: WorkSpaceResponse
    workspace_member: WorkspaceMemberResponse