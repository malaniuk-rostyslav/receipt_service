from typing import List

from pydantic import BaseModel, PositiveInt, confloat

from ...db.models.constants import PaymentType


class Product(BaseModel):
    name: str
    price: confloat(gt=0)
    quantity: PositiveInt


class Payment(BaseModel):
    payment_type: PaymentType
    amount: confloat(gt=0)


class ReceiptCreate(BaseModel):
    products: List[Product]
    payment: Payment
