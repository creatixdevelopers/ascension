from pydantic import BaseModel


class CheckoutSchema(BaseModel):
    type: str
