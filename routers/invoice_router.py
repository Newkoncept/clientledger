from fastapi import APIRouter, HTTPException
from starlette import status
from datetime import date

from models.Invoice import Invoice
from models.Workspace import Workspace
from models.Client import Client
from models.Project import Project

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from schemas.invoice_schema import (InvoiceResponse, InvoiceCreateRequest, 
                                    InvoiceUpdateRequest, InvoiceFullSummaryResponse
                                )
from utilities.helpers import item_exists_in_db, invoice_number_generator


router = APIRouter(
    prefix="/invoices",
    tags = ["invoices"]
)


@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceCreateRequest):
    workspace_exists = item_exists_in_db(db, Workspace, invoice.workspace_id, "id")
    if not workspace_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    
    client_exists = item_exists_in_db(db, Client, invoice.client_id, "id")
    if not client_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Client not found")
    
    project_exists = item_exists_in_db(db, Project, invoice.project_id, "id")
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


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_invoice(db:db_dependency, user:user_dependency, invoice:InvoiceUpdateRequest, id:int):
    invoice_exists = item_exists_in_db(db, Invoice, id, "id")
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    invoice_model = invoice.model_dump(exclude_unset=True)
    for key,value in invoice_model.items():
        setattr(invoice_exists, key, value)

    db.add(invoice_exists)
    db.commit()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(db:db_dependency, user:user_dependency, id:int):
    invoice_exists = item_exists_in_db(db, Invoice, id, "id")
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    db.delete(invoice_exists)
    db.commit()


@router.get("/workspace/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: float | None = None, due_date: date | None = None
                            ):
    
    invoice_exists = db.query(Invoice).filter(Invoice.workspace_id == id)
    if not invoice_exists.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    
    
    if invoice_status:
        invoice_exists = invoice_exists.filter(Invoice.status == invoice_status)
    if amount:
        invoice_exists = invoice_exists.filter(Invoice.amount == amount)
    if due_date:
        invoice_exists = invoice_exists.filter(Invoice.due_date == due_date)


    invoice_exists = invoice_exists.all()
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


@router.get("/client/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_client_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: float | None = None, due_date: date | None = None
                            ):
    
    invoice_exists = db.query(Invoice).filter(Invoice.client_id == id)
    if not invoice_exists.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    
    
    if invoice_status:
        invoice_exists = invoice_exists.filter(Invoice.status == invoice_status)
    if amount:
        invoice_exists = invoice_exists.filter(Invoice.amount == amount)
    if due_date:
        invoice_exists = invoice_exists.filter(Invoice.due_date == due_date)


    invoice_exists = invoice_exists.all()
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


@router.get("/project/{id}", status_code=status.HTTP_200_OK, response_model=list[InvoiceResponse])
def get_invoice_by_project_id(db:db_dependency, user:user_dependency, 
                                id:int, invoice_status: str | None = None, 
                                amount: float | None = None, due_date: date | None = None
                            ):
    
    invoice_exists = db.query(Invoice).filter(Invoice.project_id == id)
    if not invoice_exists.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    
    
    if invoice_status:
        invoice_exists = invoice_exists.filter(Invoice.status == invoice_status)
    if amount:
        invoice_exists = invoice_exists.filter(Invoice.amount == amount)
    if due_date:
        invoice_exists = invoice_exists.filter(Invoice.due_date == due_date)


    invoice_exists = invoice_exists.all()
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


@router.get("/invoice-number/{invoice_number}", status_code=status.HTTP_200_OK, response_model=InvoiceResponse)
def get_invoice_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    invoice_exists = item_exists_in_db(db, Invoice, invoice_number, "invoice_number")
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


@router.get("/invoice-id/{id}", status_code=status.HTTP_200_OK, response_model=InvoiceResponse)
def get_invoice_by_invoice_idr(db:db_dependency, user:user_dependency, id:int):
    invoice_exists = item_exists_in_db(db, Invoice, id, "id")
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")    

    return invoice_exists


@router.get("/summary/{invoice_number}", status_code=status.HTTP_200_OK, response_model=InvoiceFullSummaryResponse)
def get_invoice_summary_by_invoice_number(db:db_dependency, user:user_dependency, invoice_number:str):
    invoice_exists = item_exists_in_db(db, Invoice, invoice_number, "invoice_number")
    if not invoice_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    workspace_info = item_exists_in_db(db, Workspace, invoice_exists.workspace_id, "id")    
    client_info = item_exists_in_db(db, Client, invoice_exists.client_id, "id")    
    project_info = item_exists_in_db(db, Project, invoice_exists.project_id, "id")    

    return {
        "invoice": invoice_exists,
        "workspace": workspace_info,
        "client": client_info ,
        "project": project_info
    } 

