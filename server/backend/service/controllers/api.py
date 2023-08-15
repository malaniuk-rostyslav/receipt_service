from fastapi import APIRouter

from .auth import auth
from .products import products
from .user import user

api_router = APIRouter()

api_router.include_router(user.router, tags=["users"], prefix="/users")
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(products.router, tags=["products"], prefix="/products")
