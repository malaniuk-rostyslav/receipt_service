from fastapi import APIRouter

from .auth import auth
from .receipts import receipt
from .user import user

api_router = APIRouter()

api_router.include_router(user.router, tags=["users"], prefix="/users")
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(receipt.router, tags=["receipt"], prefix="/receipt")
