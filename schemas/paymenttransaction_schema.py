from pydantic import BaseModel
from enum import Enum

class PaymentStatus(str, Enum):
    INITIALIZED = "initialized"
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    ABANDONED = "abandoned"


class PaymentURLCreateResponse(BaseModel):
    authorization_url: str
    status: PaymentStatus


class PaymentWebhookResponse(BaseModel):
    message: str
