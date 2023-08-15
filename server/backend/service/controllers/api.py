from fastapi import APIRouter

from .user import user

api_router = APIRouter()

api_router.include_router(user.router, tags=["users"], prefix="/users")
