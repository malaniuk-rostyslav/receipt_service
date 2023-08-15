from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ....db import models
from ....db.models.constants import PaymentType
from ...core.deps import get_db, get_request_user
from ...schemas.receipt import ReceiptCreate, ReceiptResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_receipt(
    form_data: ReceiptCreate,
    current_user: models.User = Depends(get_request_user),
    db: Session = Depends(get_db),
):
    """
    Create Receipt \n
    FORM data: \n
    `products`: [ \n
        { \n
            `name`: str \n
            `price`: confloat(gt=0) \n
            `quantity`: PositiveInt \n
        } \n
    ] \n
    `payment`: { \n
        `payment_type`: PaymentType \n
        `amount`: confloat(gt=0) \n
    } \n
    Responses: \n
    `200` OK \n
    `401` Unauthorized - You did not provide authorization token or it was expired \n
    `400` BadRequest - Returns if payment amount is higher than you try to pay \n
    `422` Unprocessable Entity - Returns if wrong FORM data parameter \n
    """
    amount_to_pay = 0
    for i in form_data.products:
        amount_to_pay += i.price * i.quantity
    rest = form_data.payment.amount - amount_to_pay
    if rest < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your payment amount is higher than you try to pay",
        )
    receipt = models.Receipt(
        creator_id=current_user.id,
        payment_type=form_data.payment.payment_type,
        amount=amount_to_pay,
        total=form_data.payment.amount,
        rest=rest,
    )
    db.add(receipt)
    db.commit()
    [
        product.__dict__.update(
            {
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "total": product.price * product.quantity,
            }
        )
        for product in form_data.products
    ]
    receipt_to_return = {
        "products": [product.__dict__ for product in form_data.products],
        "payment": {
            "type": form_data.payment.payment_type,
            "amount": form_data.payment.amount,
        },
        "total": form_data.payment.amount,
        "rest": rest,
        "created_at": receipt.created_at,
    }
    return receipt_to_return


@router.get("/", response_model=Page[ReceiptResponse])
async def get_my_receipts(
    created_at: Optional[datetime] = None,
    amount: Optional[float] = None,
    payment_type: Optional[PaymentType] = None,
    current_user: models.User = Depends(get_request_user),
    db: Session = Depends(get_db),
):
    """
    Get My Receipts \n
    Query parameters: \n
    `created_at`: Optional[datetime] \n
    `amount`: Optional[float] \n
    `payment_type` Optional[PaymentType] \n
    Responses: \n
    `200` OK \n
    `401` Unauthorized - You did not provide authorization token or it was expired \n
    """
    query = db.query(models.Receipt).filter(
        models.Receipt.creator_id == current_user.id
    )
    if created_at:
        query = query.filter(models.Receipt.created_at >= created_at)
    if amount:
        query = query.filter(models.Receipt.amount >= amount)
    if payment_type:
        query = query.filter(models.Receipt.payment_type == payment_type)
    return paginate(query)
