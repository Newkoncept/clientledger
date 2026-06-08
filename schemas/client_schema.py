from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ClientCreateRequest(BaseModel):
    workspace_id: int
    name: str
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None


class ClientUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    workspace_id: int
    name: str
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime