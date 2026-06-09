from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

from schemas.client_schema import ClientResponse
from schemas.project_schema import ProjectResponse
from schemas.workspace_schema import WorkSpaceResponse


class InvoiceCreateRequest(BaseModel):
    workspace_id: int
    client_id: int 
    project_id: int
    status: str
    amount: float
    due_date: date


class InvoiceUpdateRequest(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[date] = None


class InvoiceResponse(BaseModel):
    id: int
    workspace_id: int
    client_id: int 
    project_id: int
    invoice_number: str 
    status: str
    amount: float
    due_date: date
    created_at: datetime
    updated_at: datetime


class InvoiceFullResponseBase(BaseModel):
    id: int
    invoice_number: str 
    status: str
    amount: float
    due_date: date
    created_at: datetime
    updated_at: datetime

class InvoiceFullSummaryResponse(BaseModel):
    invoice: InvoiceFullResponseBase
    workspace: WorkSpaceResponse
    client: ClientResponse 
    project: ProjectResponse