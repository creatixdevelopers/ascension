from pydantic import BaseModel
from datetime import datetime


class CheckoutSchema(BaseModel):
    type: str


class PaymentReadSchema(BaseModel):
    payment_id: str
    type: str
    created: datetime
    valid_until: datetime | None
