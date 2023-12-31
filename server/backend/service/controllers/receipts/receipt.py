from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from ....db import models
from ....db.models.constants import PaymentTypeEnum
from ...core.deps import get_current_user, get_db
from ...schemas.receipt import Receipt, ReceiptCreate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_receipt(
    form_data: ReceiptCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create Receipt \n
    JSON data: \n
    `products`: [ \n
        { \n
            `name`: str \n
            `price`: confloat(gt=0) \n
            `quantity`: PositiveInt \n
        } \n
    ] \n
    `payment`: { \n
        `payment_type`: PaymentTypeEnum \n
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
    db.flush()
    for i in form_data.products:
        product = (
            db.query(models.Product).filter(models.Product.name == i.name).one_or_none()
        )
        if not product:
            product = models.Product(
                creator_id=current_user.id, name=i.name, price=i.price
            )
            db.add(product)
            db.flush()
        receipt_history = models.ReceiptHistory(
            receipt_id=receipt.id,
            product_id=product.id,
            quantity=i.quantity,
            price=i.price,
            total=i.quantity * i.price,
        )
        db.add(receipt_history)
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
        "id": receipt.id,
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


@router.get("/", response_model=Page[Receipt])
async def get_my_receipts(
    created_at: Optional[datetime] = None,
    amount: Optional[float] = None,
    payment_type: Optional[PaymentTypeEnum] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get My Receipts \n
    Query parameters: \n
    `created_at`: Optional[datetime] \n
    `amount`: Optional[float] \n
    `payment_type` Optional[PaymentTypeEnum] \n
    Responses: \n
    `200` OK \n
    `401` Unauthorized - You did not provide authorization token or it was expired \n
    """
    receipts = db.query(models.Receipt).filter(
        models.Receipt.creator_id == current_user.id
    )
    if created_at:
        receipts = receipts.filter(models.Receipt.created_at >= created_at)
    if amount:
        receipts = receipts.filter(models.Receipt.amount >= amount)
    if payment_type:
        receipts = receipts.filter(models.Receipt.payment_type == payment_type)
    return paginate(receipts)


@router.get("/{receipt_id}", status_code=status.HTTP_200_OK)
async def get_my_text_receipt_by_id(
    receipt_id: PositiveInt,
    db: Session = Depends(get_db),
):
    """
    Get My Text Receipt By ID \n
    Path parameters: \n
    `receipt_id`: Receipt ID \n
    Responses: \n
    `200` OK \n
    `400` Not Found - Returns if Receipt not found \n
    `401` Unauthorized - You did not provide authorization token or it was expired \n
    """
    receipt = (
        db.query(models.Receipt).filter(models.Receipt.id == receipt_id).one_or_none()
    )
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found",
        )
    receipt_history = (
        db.query(models.ReceiptHistory)
        .filter(models.ReceiptHistory.receipt_id == receipt_id)
        .all()
    )
    product_info = ""
    for i in receipt_history:
        product = (
            db.query(models.Product)
            .filter(models.Product.id == i.product_id)
            .one_or_none()
        )
        product_info += (
            f"{float(i.quantity)} X {product.price}\n"
            + f"{product.name}".ljust(50 - len(f"{i.total}"))
            + f"{i.total}\n"
            + "".ljust(50, "=")
            + "\n"
        )
    text_receipt = (
        "Our shop".center(50)
        + "\n"
        + "".ljust(50, "=")
        + "\n"
        + f"{product_info}\n"
        + "Amount"
        + f"{receipt.amount}".rjust(50 - 6)
        + "\n"
        + f"{receipt.payment_type}".ljust(50 - len(f"{receipt.total}"))
        + f"{receipt.total}\n"
        + f"Rest"
        + f"{receipt.rest}".rjust(50 - 4)
        + "\n"
        + "".ljust(50, "=")
        + "\n"
        + f"{receipt.created_at.strftime('%Y-%m-%d %H:%M:%S')}".center(50)
        + "\n"
        + "Thanks for visiting us".center(50)
    )
    return PlainTextResponse(content=text_receipt)
