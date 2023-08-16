from datetime import datetime
from typing import List

from pydantic import BaseModel, PositiveInt, confloat

from ...db.models.constants import PaymentTypeEnum


class Product(BaseModel):
    name: str
    price: confloat(gt=0)
    quantity: PositiveInt


class Payment(BaseModel):
    payment_type: PaymentTypeEnum
    amount: confloat(gt=0)


class ReceiptCreate(BaseModel):
    products: List[Product]
    payment: Payment


class ReceiptResponse(BaseModel):
    id: PositiveInt
    creator_id: PositiveInt
    payment_type: PaymentTypeEnum
    amount: confloat(gt=0)
    total: confloat(gt=0)
    rest: float
    created_at: datetime
