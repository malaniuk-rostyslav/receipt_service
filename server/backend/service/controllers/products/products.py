from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....db import models
from ...core.deps import get_db, get_request_user
from ...schemas.product import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(
    form_data: ProductCreate,
    current_user: models.User = Depends(get_request_user),
    db: Session = Depends(get_db),
) -> models.Product:
    """
    Create Product \n
    FORM data: \n
    `name`: str \n
    `price`: confloat(gt=0) \n
    `quantity`: PositiveInt \n
    Responses: \n
    `200` OK \n
    `401` Unauthorized - You did not provide authorization token or it was expired \n
    `404` NotFound - Returns if NftTokenCollection was not found \n
    `422` Unprocessable Entity - Returns if wrong FORM data parameter \n
    """
    name_exists = db.query(
        db.query(models.Product).filter(models.Product.name == form_data.name).exists()
    ).scalar()
    if name_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with such name already exists",
        )
    product = models.Product(
        creator_id=current_user.id,
        name=form_data.name,
        price=form_data.price,
        quantity=form_data.quantity,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
