from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class WorkSpaceMemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    STAFF = "staff"


class WorkspaceMemberRequest(BaseModel):
    workspace_id:int = Field(gt=0)
    user_id:int = Field(gt=0)
    role:WorkSpaceMemberRole


class WorkspaceMemberDeleteRequest(BaseModel):
    workspace_id:int = Field(gt=0)
    user_id:int = Field(gt=0)


class WorkspaceMemberUpdateRequest(BaseModel):
    role:WorkSpaceMemberRole


class WorkspaceMemberResponse(BaseModel):
    id:int
    workspace_id:int
    user_id:int
    role:WorkSpaceMemberRole
    created_at:datetime
    updated_at:datetime

    model_config = {
        "from_attributes": True
    }
