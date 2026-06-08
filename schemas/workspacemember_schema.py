from pydantic import BaseModel, Field
from datetime import datetime


class WorkspaceMemberRequest(BaseModel):
    workspace_id:int = Field(gt=0)
    user_id:int = Field(gt=0)
    role:str = Field(min_length=3)



class WorkspaceMemberDeleteRequest(BaseModel):
    workspace_id:int = Field(gt=0)
    user_id:int = Field(gt=0)


class WorkspaceMemberUpdateRequest(BaseModel):
    role:str = Field(min_length=3)



class WorkspaceMemberResponse(BaseModel):
    id:int = Field()
    workspace_id:int = Field()
    user_id:int = Field()
    role:str = Field()
    created_at:datetime = Field()
    updated_at:datetime = Field()