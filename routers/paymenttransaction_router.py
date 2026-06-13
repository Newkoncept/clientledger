from fastapi import APIRouter, Request
from starlette import status
from dependencies.db_dependency import db_dependency
from services import paymenttransaction_service
from schemas.paymenttransaction_schema import PaymentURLCreateResponse, PaymentWebhookResponse


router = APIRouter(
    prefix="/payments/paystack",
    tags = ["Payment Transactions"]
)


@router.post("/initialize", response_model=PaymentURLCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_payment_record(db:db_dependency, invoice_number:str):
    return await paymenttransaction_service.create_payment_record(db, invoice_number)


@router.post("/webhook", status_code= status.HTTP_200_OK, response_model=PaymentWebhookResponse)
async def payment_webhook(db:db_dependency, request: Request):
    return await paymenttransaction_service.payment_webhook(db, request)