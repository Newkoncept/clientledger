from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class ClientCreateRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(min_length=5, max_length=100, default= None)
    company_name: Optional[str] = Field(min_length=5, max_length=100, default = None)


class ClientUpdateRequest(BaseModel):
    name: Optional[str] = Field(min_length=5, max_length=100, default = None)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(min_length=5, max_length=100, default = None)
    company_name: Optional[str] = Field(min_length=5, max_length=100, default = None)


class ClientResponse(BaseModel):
    id: int
    workspace_id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
