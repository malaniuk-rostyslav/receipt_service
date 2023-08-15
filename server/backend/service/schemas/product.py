from pydantic import BaseModel, PositiveInt, confloat


class ProductCreate(BaseModel):
    name: str
    price: confloat(gt=0)
    quantity: PositiveInt


class ProductResponse(ProductCreate):
    name: str
    price: confloat(gt=0)
    quantity: PositiveInt
    creator_id: PositiveInt
