from database import Base
from sqlalchemy import Column, String, Integer, func, ForeignKey, DateTime


class PaymentTransaction(Base):
    __tablename__ = "paymenttransactions"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    provider = Column(String, nullable=False,default="paystack")
    reference = Column(String, nullable=False, unique=True, index=True)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False, default="NGN")
    status = Column(String, nullable=False, index=True)
    authorization_url = Column(String, nullable=True)
    paid_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    