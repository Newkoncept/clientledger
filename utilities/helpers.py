from decimal import Decimal
import uuid, secrets
from datetime import date, datetime
import requests

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from utilities.user_utilities import create_access_token



def get_db_item_by_column(db:Session, model, column_name:str, value):
    column = getattr(model, column_name, None)
    return db.query(model).filter(column == value).first()


def invoice_number_generator(workspace_id:int):
    INVOICE_PREFIX = "INV"
    year = datetime.now().year
    unique_value = uuid.uuid4().hex.upper()

    return f'{INVOICE_PREFIX}-{year}-WS{workspace_id}-{unique_value[:4]}-{unique_value[4:8]}-{unique_value[8:12]}'


def payment_reference_generator(invoice_number:str):
    return f'PAY-{invoice_number}-{(secrets.token_hex()[5:12]).upper()}'


def login_token_generator(user_id:int, time_allowed):
    token = create_access_token(user_id, time_allowed)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def invoice_search_filter(db: Session, model, base_column, id:int, 
                          invoice_status: str | None = None, amount: Decimal | None = None, 
                          due_date: date | None = None):
    
    invoice_exists = db.query(model).filter(getattr(model, base_column, None) == id)

    if invoice_status:
        invoice_exists = invoice_exists.filter(getattr(model, "status", None) == invoice_status)
    if amount:
        invoice_exists = invoice_exists.filter(getattr(model, "amount", None) == amount)
    if due_date:
        invoice_exists = invoice_exists.filter(getattr(model, "due_date", None) == due_date)

    return invoice_exists.all()


def project_search_filter(db:Session, model, base_column:str, id:int, name:str | None = None, project_status:str | None= None,
                          start_date:date | None= None, due_date:date | None= None):
    project_exists= db.query(model).filter(getattr(model, base_column, None) == id)

    if name:
        project_exists = project_exists.filter(getattr(model, "name", None) == name)
    if project_status:
        project_exists = project_exists.filter(getattr(model, "status", None) == project_status)
    if start_date:
        project_exists = project_exists.filter(getattr(model, "start_date", None) == start_date)
    if due_date:
        project_exists = project_exists.filter(getattr(model, "due_date", None) == due_date)
    
    return project_exists.all()


def get_or_404(db:Session, model, column_name:str, value, message:str):
    model_exists = get_db_item_by_column(db, model, column_name, value)
    if not model_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= message)
    return model_exists


def verify_paystack_transaction(url: str, key: str) -> dict:
    headers = {
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not verify Paystack transaction")

    response_data = response.json()
    if not response_data.get("status"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_data.get("message", "Paystack verification failed"))

    return response_data["data"]
