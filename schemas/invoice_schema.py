from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum

from schemas.client_schema import ClientResponse
from schemas.project_schema import ProjectResponse
from schemas.workspace_schema import WorkSpaceResponse


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class InvoiceCreateRequest(BaseModel):
    workspace_id: int = Field(gt = 0)
    client_id: int = Field(gt = 0)
    project_id: int = Field(gt = 0)
    status: InvoiceStatus 
    amount: Decimal = Field(gt = 0, decimal_places=2)
    due_date: date


class InvoiceUpdateRequest(BaseModel):
    status: InvoiceStatus | None = None
    amount: Decimal | None = Field(gt = 0, default = None, decimal_places=2)
    due_date: date | None = None


class InvoiceResponse(BaseModel):
    id: int
    workspace_id: int
    client_id: int 
    project_id: int
    invoice_number: str 
    status: InvoiceStatus
    amount: Decimal
    due_date: date
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }



class InvoiceFullResponseBase(BaseModel):
    id: int
    invoice_number: str 
    status: InvoiceStatus
    amount: Decimal
    due_date: date
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }



class InvoiceFullSummaryResponse(BaseModel):
    invoice: InvoiceFullResponseBase
    workspace: WorkSpaceResponse
    client: ClientResponse 
    project: ProjectResponse

    model_config = {
        "from_attributes": True
    }
