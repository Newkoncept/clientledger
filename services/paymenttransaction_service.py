from datetime import datetime, timezone
from fastapi import HTTPException, Request
from starlette import status
from sqlalchemy.orm import Session
import httpx, os, hashlib, hmac
from dotenv import load_dotenv

from models.Invoice import Invoice
from models.Client import Client
from models.PaymentTransaction import PaymentTransaction

from schemas.invoice_schema import InvoiceStatus
from schemas.paymenttransaction_schema import PaymentStatus

from utilities.helpers import get_db_item_by_column, payment_reference_generator, verify_paystack_transaction

load_dotenv()

PAYSTACK_INITIALIZE_URL = os.getenv("PAYSTACK_INITIALIZE_URL")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_REFERENCE_URL = os.getenv("PAYSTACK_REFERENCE_URL")

if not PAYSTACK_SECRET_KEY or not PAYSTACK_INITIALIZE_URL or not PAYSTACK_REFERENCE_URL:
    raise RuntimeError("PAYSTACK ENV VARS NOT FOUND")


async def create_payment_record(db:Session, invoice_number:str):
    invoice_exists:Invoice = get_db_item_by_column(db, Invoice, "invoice_number", invoice_number)

    if not invoice_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    if invoice_exists.status == InvoiceStatus.PAID or invoice_exists.status == InvoiceStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invoice has been {invoice_exists.status}") 
    
    payment_active = (
                        db.query(PaymentTransaction)
                        .filter(PaymentTransaction.invoice_id == invoice_exists.id)
                        .order_by(PaymentTransaction.created_at.desc())
                        .first()
                    )
    
    if payment_active:
        if payment_active.status == PaymentStatus.SUCCESS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invoice has been paid") 
        if payment_active.status == PaymentStatus.PENDING:
            return {
                "authorization_url" : payment_active.authorization_url,
                "status" : payment_active.status
            }
    
    client_exists:Client = get_db_item_by_column(db, Client, "id", invoice_exists.client_id)
    if not client_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    
    payment_transaction_model = PaymentTransaction()
    payment_transaction_model.invoice_id = invoice_exists.id
    payment_transaction_model.workspace_id = invoice_exists.workspace_id
    payment_transaction_model.client_id = invoice_exists.client_id
    payment_transaction_model.amount = int(invoice_exists.amount * 100)
    payment_transaction_model.reference = payment_reference_generator(invoice_number)
    payment_transaction_model.status = PaymentStatus.INITIALIZED

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = { 
        "email": client_exists.email, 
        "amount": payment_transaction_model.amount,
        "channels": ["card", "bank", "ussd", "qr", "bank_transfer"],
        "reference": payment_transaction_model.reference
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(PAYSTACK_INITIALIZE_URL,headers=headers, json=data)

        result = response.json()

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=result)

        payment_transaction_model.authorization_url = result["data"]["authorization_url"]
        payment_transaction_model.status = PaymentStatus.PENDING
    
        db.add(payment_transaction_model)
        db.commit()
        db.refresh(payment_transaction_model)

        return {
            "authorization_url" : payment_transaction_model.authorization_url,
            "status" : payment_transaction_model.status
        }
    
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not reach Paystack: {exc}")
    

async def payment_webhook(db:Session, request:Request):
    raw_body = await request.body()

    paystack_signature = request.headers.get("x-paystack-signature")
    if not paystack_signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Paystack signature")

    computed_signature = hmac.new(PAYSTACK_SECRET_KEY.encode("utf-8"), raw_body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(computed_signature, paystack_signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Paystack signature")

    payload = await request.json()
    event = payload.get("event")
    data = payload.get("data", {})

    if event != "charge.success":
        return {"message": "Event ignored"}

    reference = data.get("reference")
    if not reference:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing payment reference")

    payment = db.query(PaymentTransaction).filter(PaymentTransaction.reference == reference).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment transaction not found")

    if payment.status == PaymentStatus.SUCCESS:
        return {"message": "Payment already processed"}

    verification_URL = f"{PAYSTACK_REFERENCE_URL}/{reference}"
    verified_data = verify_paystack_transaction(verification_URL, PAYSTACK_SECRET_KEY)
    paystack_status = verified_data.get("status")
    paystack_amount = verified_data.get("amount")
    paystack_currency = verified_data.get("currency")
    paystack_reference = verified_data.get("reference")

    if paystack_reference != payment.reference:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment reference mismatch")

    if paystack_amount != payment.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment amount mismatch")

    if paystack_currency != payment.currency:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment currency mismatch")

    if paystack_status != PaymentStatus.SUCCESS:
        payment.status = PaymentStatus.FAILED
        db.commit()
        return {"message": "Payment not successful"}

    payment.status = PaymentStatus.SUCCESS
    payment.paid_at = datetime.now(timezone.utc)

    invoice = db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
    if invoice:
        invoice.status = InvoiceStatus.PAID

    db.commit()
    return {"message": "Payment verified successfully"}
