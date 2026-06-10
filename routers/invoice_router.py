from fastapi import APIRouter
from starlette import status
from datetime import date
from decimal import Decimal

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from schemas.invoice_schema import (InvoiceResponse, InvoiceCreateRequest, 
                                    InvoiceUpdateRequest, InvoiceFullSummaryResponse
                                )
from services import invoice_service

router = APIRouter(
    prefix="/invoices",
    tags = ["invoices"]
)


@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceCreateRequest):
    return invoice_service.create_invoice(db, user, invoice)


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceUpdateRequest, id:int):
    invoice_service.update_invoice(db, user, invoice, id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(db:db_dependency, user:user_dependency, id:int):
    invoice_service.delete_invoice(db, user, id)

@router.get("/workspace/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    return invoice_service.get_invoice_by_workspace_id(db, user, id, invoice_status, amount, due_date)


@router.get("/client/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_client_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    return invoice_service.get_invoice_by_client_id(db, user, id, invoice_status, amount, due_date)


@router.get("/project/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_project_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    return invoice_service.get_invoice_by_project_id(db, user, id, invoice_status, amount, due_date)


@router.get("/by-number/{invoice_number}", status_code=status.HTTP_200_OK, response_model=InvoiceResponse)
def get_invoice_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    return invoice_service.get_invoice_by_invoice_number(db, user, invoice_number)


@router.get("/summary/{invoice_number}", status_code=status.HTTP_200_OK, response_model=InvoiceFullSummaryResponse)
def get_invoice_summary_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    return invoice_service.get_invoice_summary_by_invoice_number(db, user, invoice_number)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=InvoiceResponse)
def get_invoice_by_invoice_id(db:db_dependency, user:user_dependency, id:int):
    return invoice_service.get_invoice_by_invoice_id(db, user, id)

