from fastapi import APIRouter
from starlette import status
from datetime import date
from decimal import Decimal

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency
from dependencies.permission import STAFF, ADMIN

from schemas.invoice_schema import (InvoiceResponse, InvoiceCreateRequest, InvoiceStatus, 
                                    InvoiceUpdateRequest, InvoiceFullSummaryResponse
                                )
from services import invoice_service

router = APIRouter(
    prefix="/invoices",
    tags = ["invoices"]
)


@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceCreateRequest):
    return invoice_service.create_invoice(db, user, invoice, STAFF)


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceUpdateRequest, id:int):
    invoice_service.update_invoice(db, user, invoice, id, STAFF)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(db:db_dependency, user:user_dependency, id:int):
    invoice_service.delete_invoice(db, user, id, ADMIN)

@router.get("/workspace/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: InvoiceStatus | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    return invoice_service.get_invoice_by_workspace_id(db, user, id, invoice_status, amount, due_date, STAFF)


@router.get("/client/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_client_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: InvoiceStatus | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    return invoice_service.get_invoice_by_client_id(db, user, id, invoice_status, amount, due_date, STAFF)


@router.get("/project/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_project_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: InvoiceStatus | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    return invoice_service.get_invoice_by_project_id(db, user, id, invoice_status, amount, due_date, STAFF)


@router.get("/by-number/{invoice_number}", status_code=status.HTTP_200_OK, response_model=InvoiceResponse)
def get_invoice_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    return invoice_service.get_invoice_by_invoice_number(db, user, invoice_number, STAFF)


@router.get("/summary/{invoice_number}", status_code=status.HTTP_200_OK, response_model=InvoiceFullSummaryResponse)
def get_invoice_summary_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    return invoice_service.get_invoice_summary_by_invoice_number(db, user, invoice_number, STAFF)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=InvoiceResponse)
def get_invoice_by_invoice_id(db:db_dependency, user:user_dependency, id:int):
    return invoice_service.get_invoice_by_invoice_id(db, user, id, STAFF)

