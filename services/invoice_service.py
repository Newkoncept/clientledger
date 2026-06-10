from fastapi import HTTPException
from starlette import status
from datetime import date
from decimal import Decimal

from models.Invoice import Invoice
from models.Workspace import Workspace
from models.Client import Client
from models.Project import Project

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from schemas.invoice_schema import InvoiceCreateRequest, InvoiceUpdateRequest
from utilities.helpers import get_db_item_by_column, invoice_number_generator, invoice_search_filter



def create_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceCreateRequest):
    workspace_exists = get_db_item_by_column(db, Workspace, "id", invoice.workspace_id)
    if not workspace_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    
    client_exists = get_db_item_by_column(db, Client, "id", invoice.client_id)
    if not client_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Client not found")
    
    project_exists = get_db_item_by_column(db, Project, "id", invoice.project_id)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")    
    if project_exists.client_id != invoice.client_id :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project is not linked to client")
    if project_exists.workspace_id != invoice.workspace_id:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project is not linked to workspace")
    

    invoice_model = Invoice(**invoice.model_dump())
    invoice_model.invoice_number = invoice_number_generator(invoice.workspace_id)

    db.add(invoice_model)
    db.commit()
    db.refresh(invoice_model)

    return invoice_model


def update_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceUpdateRequest, id:int):
    invoice_exists = get_db_item_by_column(db, Invoice, "id", id)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    invoice_model = invoice.model_dump(exclude_unset=True)
    for key,value in invoice_model.items():
        setattr(invoice_exists, key, value)

    db.add(invoice_exists)
    db.commit()


def delete_invoice(db:db_dependency, user:user_dependency, id:int):
    invoice_exists = get_db_item_by_column(db, Invoice, "id", id)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    db.delete(invoice_exists)
    db.commit()


def get_invoice_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):
    invoice_exists = invoice_search_filter(db, Invoice, "workspace_id", id, invoice_status, amount, due_date)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    
    return invoice_exists


def get_invoice_by_client_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):    
    
    invoice_exists = invoice_search_filter(db, Invoice, "client_id", id, invoice_status, amount, due_date)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


def get_invoice_by_project_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: Decimal | None = None, due_date: date | None = None):

    invoice_exists = invoice_search_filter(db, Invoice, "project_id", id, invoice_status, amount, due_date)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


def get_invoice_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    invoice_exists = get_db_item_by_column(db, Invoice, "invoice_number", invoice_number)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


def get_invoice_by_invoice_id(db:db_dependency, user:user_dependency, id:int):
    invoice_exists = get_db_item_by_column(db, Invoice, "id", id)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


def get_invoice_summary_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    invoice_exists = get_db_item_by_column(db, Invoice, "invoice_number", invoice_number)
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    workspace_info = get_db_item_by_column(db, Workspace, "id", invoice_exists.workspace_id)
    client_info = get_db_item_by_column(db, Client, "id", invoice_exists.client_id)
    project_info = get_db_item_by_column(db, Project, "id", invoice_exists.project_id)

    return {
        "invoice": invoice_exists,
        "workspace": workspace_info,
        "client": client_info ,
        "project": project_info
    } 

